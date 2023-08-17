"""
### 计划任务相关
"""
import asyncio
import random
import threading
from typing import Union, Optional

from nonebot import on_command, get_adapters
from nonebot.adapters.onebot.v11 import MessageSegment as OneBotV11MessageSegment, Adapter as OneBotV11Adapter, \
    MessageEvent as OneBotV11MessageEvent
from nonebot.adapters.qqguild import MessageSegment as QQGuildMessageSegment, Adapter as QQGuildAdapter, \
    MessageEvent as QQGuildMessageEvent
from nonebot.adapters.qqguild.exception import AuditException
from nonebot.exception import ActionFailed
from nonebot.internal.matcher import Matcher
from nonebot_plugin_apscheduler import scheduler

from .data_model import MissionStatus
from .exchange import generate_image
from .game_sign_api import BaseGameSign
from .myb_missions_api import BaseMission, get_missions_state
from .plugin_data import PluginDataManager, write_plugin_data
from .simple_api import genshin_board, get_game_record, StarRail_board
from .utils import get_file, logger, COMMAND_BEGIN, GeneralMessageEvent, send_private_msg

_conf = PluginDataManager.plugin_data

manually_game_sign = on_command(_conf.preference.command_start + '签到', priority=5, block=True)
manually_game_sign.name = '签到'
manually_game_sign.usage = '手动进行游戏签到，查看本次签到奖励及本月签到天数'


@manually_game_sign.handle()
async def _(event: Union[GeneralMessageEvent], matcher: Matcher):
    """
    手动游戏签到函数
    """
    user = _conf.users.get(event.get_user_id())
    if not user or not user.accounts:
        await manually_game_sign.finish(f"⚠️你尚未绑定米游社账户，请先使用『{COMMAND_BEGIN}登录』进行登录")
    await manually_game_sign.send("⏳开始游戏签到...")
    await perform_game_sign(user_id=event.get_user_id(), matcher=matcher, event=event)


manually_bbs_sign = on_command(_conf.preference.command_start + '任务', priority=5, block=True)
manually_bbs_sign.name = '任务'
manually_bbs_sign.usage = '手动执行米游币每日任务，可以查看米游币任务完成情况'


@manually_bbs_sign.handle()
async def _(event: Union[GeneralMessageEvent], matcher: Matcher):
    """
    手动米游币任务函数
    """
    user = _conf.users.get(event.get_user_id())
    if not user or not user.accounts:
        await manually_game_sign.finish(f"⚠️你尚未绑定米游社账户，请先使用『{COMMAND_BEGIN}登录』进行登录")
    await manually_game_sign.send("⏳开始执行米游币任务...")
    await perform_bbs_sign(user_id=event.get_user_id(), matcher=matcher)


manually_resin_check = on_command(
    _conf.preference.command_start + '原神便笺',
    aliases={
        _conf.preference.command_start + '便笺',
        _conf.preference.command_start + '便签',
        _conf.preference.command_start + '原神便签',
    },
    priority=5,
    block=True
)
manually_resin_check.name = '原神便笺'
manually_resin_check.usage = '手动查看原神实时便笺，即原神树脂、洞天财瓮等信息'
has_checked = {}
for user in _conf.users.values():
    for account in user.accounts.values():
        if account.enable_resin:
            has_checked[account.bbs_uid] = has_checked.get(account.bbs_uid,
                                                           {"resin": False, "coin": False, "transformer": False})


@manually_resin_check.handle()
async def _(event: Union[GeneralMessageEvent], matcher: Matcher):
    """
    手动查看原神便笺
    """
    user = _conf.users.get(event.get_user_id())
    if not user or not user.accounts:
        await manually_game_sign.finish(f"⚠️你尚未绑定米游社账户，请先使用『{COMMAND_BEGIN}登录』进行登录")
    await resin_check(user_id=event.get_user_id(), matcher=matcher)


manually_resin_check_sr = on_command(
    _conf.preference.command_start + '星穹铁道便笺',
    aliases={
        _conf.preference.command_start + '铁道便笺',
        _conf.preference.command_start + '铁道便签',
    },
    priority=5,
    block=True
)
manually_resin_check_sr.name = '星穹铁道便笺'
manually_resin_check_sr.usage = '手动查看星穹铁道实时便笺，即开拓力、每日实训、每周模拟宇宙积分等信息'
for user in _conf.users.values():
    for account in user.accounts.values():
        if account.enable_resin:
            has_checked[account.bbs_uid] = has_checked.get(account.bbs_uid,
                                                           {"stamina": False, "train_score": False,
                                                            "rogue_score": False})


@manually_resin_check_sr.handle()
async def _(event: Union[GeneralMessageEvent], matcher: Matcher):
    """
    手动查看星穹铁道便笺（sr）
    """
    user = _conf.users.get(event.get_user_id())
    if not user or not user.accounts:
        await manually_game_sign.finish(f"⚠️你尚未绑定米游社账户，请先使用『{COMMAND_BEGIN}登录』进行登录")
    await resin_check_sr(user_id=event.get_user_id(), matcher=matcher)


async def perform_game_sign(user_id: str, matcher: Matcher = None, event: Union[GeneralMessageEvent] = None):
    """
    执行游戏签到函数，并发送给用户签到消息。

    :param user_id: 用户QQ号
    :param matcher: 事件响应器
    :param event: 事件
    """
    failed_accounts = []
    user = _conf.users[user_id]
    for account in _conf.users.get(user_id).accounts.values():
        # 自动签到时，要求用户打开了签到功能；手动签到时都可以调用执行。
        if not matcher and not account.enable_game_sign:
            continue
        signed = False
        """是否已经完成过签到"""
        game_record_status, records = await get_game_record(account)
        if not game_record_status:
            if matcher:
                await matcher.send(f"⚠️账户 {account.bbs_uid} 获取游戏账号信息失败，请重新尝试")
            else:
                await send_private_msg(
                    user_id=user_id,
                    message=f"⚠️账户 {account.bbs_uid} 获取游戏账号信息失败，请重新尝试"
                )
            continue
        games_has_record = []
        for class_type in BaseGameSign.AVAILABLE_GAME_SIGNS:
            signer = class_type(account, records)
            if not signer.has_record:
                continue
            else:
                games_has_record.append(signer)
            get_info_status, info = await signer.get_info(account.platform)
            if not get_info_status:
                if matcher:
                    await matcher.send(f"⚠️账户 {account.bbs_uid} 获取签到记录失败")
                else:
                    await send_private_msg(
                        user_id=user_id,
                        message=f"⚠️账户 {account.bbs_uid} 获取签到记录失败"
                    )
            else:
                signed = info.is_sign

            # 若没签到，则进行签到功能；若获取今日签到情况失败，仍可继续
            if (get_info_status and not info.is_sign) or not get_info_status:
                if matcher:
                    sign_status = await signer.sign(
                        account.platform,
                        matcher.send("⏳正在尝试完成人机验证，请稍后...")
                    )
                else:
                    sign_status = await signer.sign(account.platform)
                if not sign_status and (user.enable_notice or matcher):
                    if sign_status.login_expired:
                        message = f"⚠️账户 {account.bbs_uid} 🎮『{signer.NAME}』签到时服务器返回登录失效，请尝试重新登录绑定账户"
                    elif sign_status.need_verify:
                        message = f"⚠️账户 {account.bbs_uid} 🎮『{signer.NAME}』签到时可能遇到验证码拦截，请尝试使用命令『/账号设置』更改设备平台，若仍失败请手动前往米游社签到"
                    else:
                        message = f"⚠️账户 {account.bbs_uid} 🎮『{signer.NAME}』签到失败，请稍后再试"
                    if matcher:
                        await matcher.send(message)
                    elif user.enable_notice:
                        await send_private_msg(user_id=user_id, message=message)
                    await asyncio.sleep(_conf.preference.sleep_time)
                    continue

                await asyncio.sleep(_conf.preference.sleep_time)

            # 用户打开通知或手动签到时，进行通知
            if user.enable_notice or matcher:
                onebot_img_msg, qq_guild_img_msg = "", ""
                get_info_status, info = await signer.get_info(account.platform)
                get_award_status, awards = await signer.get_rewards()
                if not get_info_status or not get_award_status:
                    msg = f"⚠️账户 {account.bbs_uid} 🎮『{signer.NAME}』获取签到结果失败！请手动前往米游社查看"
                else:
                    award = awards[info.total_sign_day - 1]
                    if info.is_sign:
                        status = "签到成功！" if not signed else "已经签到过了"
                        msg = f"🪪账户 {account.bbs_uid}" \
                              f"\n🎮『{signer.NAME}』" \
                              f"\n🎮状态: {status}" \
                              f"\n{signer.record.nickname}·{signer.record.level}" \
                              "\n\n🎁今日签到奖励：" \
                              f"\n{award.name} * {award.cnt}" \
                              f"\n\n📅本月签到次数：{info.total_sign_day}"
                        img_file = await get_file(award.icon)
                        onebot_img_msg = OneBotV11MessageSegment.image(img_file)
                        qq_guild_img_msg = QQGuildMessageSegment.file_image(img_file)
                    else:
                        msg = f"⚠️账户 {account.bbs_uid} 🎮『{signer.NAME}』签到失败！请尝试重新签到，若多次失败请尝试重新登录绑定账户"
                if matcher:
                    try:
                        if isinstance(event, OneBotV11MessageEvent):
                            await matcher.send(msg + onebot_img_msg)
                        elif isinstance(event, QQGuildMessageEvent):
                            await matcher.send(msg)
                            await matcher.send(qq_guild_img_msg)
                    except (ActionFailed, AuditException):
                        pass
                else:
                    for adapter in get_adapters().values():
                        try:
                            if isinstance(adapter, OneBotV11Adapter):
                                await send_private_msg(use=adapter, user_id=user_id, message=msg + onebot_img_msg)
                            elif isinstance(adapter, QQGuildAdapter):
                                await send_private_msg(use=adapter, user_id=user_id, message=msg)
                                await send_private_msg(use=adapter, user_id=user_id, message=qq_guild_img_msg)
                        except (ActionFailed, AuditException):
                            pass
            await asyncio.sleep(_conf.preference.sleep_time)

        if not games_has_record:
            if matcher:
                await matcher.send(f"⚠️您的米游社账户 {account.bbs_uid} 下不存在任何游戏账号，已跳过签到")
            else:
                await send_private_msg(user_id=user_id,
                                       message=f"⚠️您的米游社账户 {account.bbs_uid} 下不存在任何游戏账号，已跳过签到")

    # 如果全部登录失效，则关闭通知
    if len(failed_accounts) == len(user.accounts):
        user.enable_notice = False
        write_plugin_data()


async def perform_bbs_sign(user_id: str, matcher: Matcher = None):
    """
    执行米游币任务函数，并发送给用户任务执行消息。

    :param user_id: 用户QQ号
    :param matcher: 事件响应器
    """
    failed_accounts = []
    user = _conf.users[user_id]
    for account in user.accounts.values():
        # 自动执行米游币任务时，要求用户打开了米游币任务功能；手动执行米游币任务时都可以调用执行。
        if not matcher and not account.enable_mission:
            continue

        missions_state_status, missions_state = await get_missions_state(account)
        if not missions_state_status:
            if missions_state_status.login_expired:
                if matcher:
                    await matcher.send(f'⚠️账户 {account.bbs_uid} 登录失效，请重新登录')
                else:
                    await send_private_msg(user_id=user_id, message=f'⚠️账户 {account.bbs_uid} 登录失效，请重新登录')
                continue
            if matcher:
                await matcher.send(f'⚠️账户 {account.bbs_uid} 获取任务完成情况请求失败，你可以手动前往App查看')
            else:
                await send_private_msg(user_id=user_id,
                                       message=f'⚠️账户 {account.bbs_uid} 获取任务完成情况请求失败，你可以手动前往App查看')
            continue
        myb_before_mission = missions_state.current_myb

        # 在此处进行判断。因为如果在多个分区执行任务，会在完成之前就已经达成米游币任务目标，导致其他分区任务不会执行。
        finished = all(current == mission.threshold for mission, current in missions_state.state_dict.values())
        if not finished:
            for class_type in account.mission_games:
                mission_obj: BaseMission = class_type(account)
                if matcher:
                    await matcher.send(f'🆔账户 {account.bbs_uid} ⏳开始在分区『{class_type.NAME}』执行米游币任务...')

                # 执行任务
                sign_status, read_status, like_status, share_status = (
                    MissionStatus(),
                    MissionStatus(),
                    MissionStatus(),
                    MissionStatus()
                )
                sign_points: Optional[int] = None
                for key_name in missions_state.state_dict:
                    if key_name == BaseMission.SIGN:
                        sign_status, sign_points = await mission_obj.sign()
                    elif key_name == BaseMission.VIEW:
                        read_status = await mission_obj.read()
                    elif key_name == BaseMission.LIKE:
                        like_status = await mission_obj.like()
                    elif key_name == BaseMission.SHARE:
                        share_status = await mission_obj.share()

                if matcher:
                    await matcher.send(
                        f"🆔账户 {account.bbs_uid} 🎮『{class_type.NAME}』米游币任务执行情况：\n"
                        f"📅签到：{'✓' if sign_status else '✕'} +{sign_points or '0'} 米游币🪙\n"
                        f"📰阅读：{'✓' if read_status else '✕'}\n"
                        f"❤️点赞：{'✓' if like_status else '✕'}\n"
                        f"↗️分享：{'✓' if share_status else '✕'}"
                    )

        # 用户打开通知或手动任务时，进行通知
        if user.enable_notice or matcher:
            missions_state_status, missions_state = await get_missions_state(account)
            if not missions_state_status:
                if missions_state_status.login_expired:
                    if matcher:
                        await matcher.send(f'⚠️账户 {account.bbs_uid} 登录失效，请重新登录')
                    else:
                        await send_private_msg(user_id=user_id,
                                               message=f'⚠️账户 {account.bbs_uid} 登录失效，请重新登录')
                    continue
                if matcher:
                    await matcher.send(
                        f'⚠️账户 {account.bbs_uid} 获取任务完成情况请求失败，你可以手动前往App查看')
                else:
                    await send_private_msg(user_id=user_id,
                                           message=f'⚠️账户 {account.bbs_uid} 获取任务完成情况请求失败，你可以手动前往App查看')
                continue
            if all(current == mission.threshold for mission, current in missions_state.state_dict.values()):
                notice_string = "🎉已完成今日米游币任务"
            else:
                notice_string = "⚠️今日米游币任务未全部完成"

            msg = f"{notice_string}" \
                  f"\n🆔账户 {account.bbs_uid}"
            for key_name, (mission, current) in missions_state.state_dict.items():
                if key_name == BaseMission.SIGN:
                    mission_name = "📅签到"
                elif key_name == BaseMission.VIEW:
                    mission_name = "📰阅读"
                elif key_name == BaseMission.LIKE:
                    mission_name = "❤️点赞"
                elif key_name == BaseMission.SHARE:
                    mission_name = "↗️分享"
                else:
                    mission_name = mission.mission_key
                msg += f"\n{mission_name}：{'✓' if current >= mission.threshold else '✕'}"
            msg += f"\n🪙获得米游币: {missions_state.current_myb - myb_before_mission}" \
                   f"\n💰当前米游币: {missions_state.current_myb}"

            if matcher:
                await matcher.send(msg)
            else:
                await send_private_msg(user_id=user_id, message=msg)

    # 如果全部登录失效，则关闭通知
    if len(failed_accounts) == len(user.accounts):
        user.enable_notice = False
        write_plugin_data()


async def resin_check(user_id: str, matcher: Matcher = None):
    """
    查看原神实时便笺函数，并发送给用户任务执行消息。

    :param user_id: 用户QQ号
    :param matcher: 事件响应器
    """
    global has_checked
    user = _conf.users[user_id]
    for account in user.accounts.values():
        if account.enable_resin:
            has_checked[account.bbs_uid] = has_checked.get(account.bbs_uid,
                                                           {"resin": False, "coin": False, "transformer": False})
        if account.enable_resin or matcher:
            genshin_board_status, board = await genshin_board(account)
            if not genshin_board_status:
                if genshin_board_status.login_expired:
                    if matcher:
                        await matcher.send(f'⚠️账户 {account.bbs_uid} 登录失效，请重新登录')
                if genshin_board_status.no_genshin_account:
                    if matcher:
                        await matcher.send(f'⚠️账户 {account.bbs_uid} 没有绑定任何原神账户，请绑定后再重试')
                    account.enable_resin = False
                    write_plugin_data()
                    continue
                if matcher:
                    await matcher.send(f'⚠️账户 {account.bbs_uid} 获取实时便笺请求失败，你可以手动前往App查看')
                continue
            if genshin_board_status.need_verify:
                if matcher:
                    await matcher.send('⚠️遇到验证码正在尝试绕过')
            msg = ''
            # 手动查询体力时，无需判断是否溢出
            if not matcher:
                # 体力溢出提醒
                if board.current_resin == 160:
                    # 防止重复提醒
                    if has_checked[account.bbs_uid]['resin']:
                        return
                    else:
                        has_checked[account.bbs_uid]['resin'] = True
                        msg += '❕您的树脂已经满啦\n'
                else:
                    has_checked[account.bbs_uid]['resin'] = False
                # 洞天财瓮溢出提醒
                if board.current_home_coin == board.max_home_coin:
                    # 防止重复提醒
                    if has_checked[account.bbs_uid]['coin']:
                        return
                    else:
                        has_checked[account.bbs_uid]['coin'] = True
                        msg += '❕您的洞天财瓮已经满啦\n'
                else:
                    has_checked[account.bbs_uid]['coin'] = False
                # 参量质变仪就绪提醒
                if board.transformer:
                    if board.transformer_text == '已准备就绪':
                        # 防止重复提醒
                        if has_checked[account.bbs_uid]['transformer']:
                            return
                        else:
                            has_checked[account.bbs_uid]['transformer'] = True
                            msg += '❕您的参量质变仪已准备就绪\n\n'
                    else:
                        has_checked[account.bbs_uid]['transformer'] = False
                        return
                else:
                    has_checked[account.bbs_uid]['transformer'] = True
            msg += "❖实时便笺❖" \
                   f"\n⏳树脂数量：{board.current_resin} / 160" \
                   f"\n⏱️树脂{board.resin_recovery_text}" \
                   f"\n🕰️探索派遣：{board.current_expedition_num} / {board.max_expedition_num}" \
                   f"\n📅每日委托：{4 - board.finished_task_num} 个任务未完成" \
                   f"\n💰洞天财瓮：{board.current_home_coin} / {board.max_home_coin}" \
                   f"\n🎰参量质变仪：{board.transformer_text if board.transformer else 'N/A'}"
            if matcher:
                await matcher.send(msg)
            else:
                if board.current_resin >= account.user_resin_threshold:
                    await send_private_msg(user_id=user_id, message=msg)
                else:
                    logger.info(f"原神实时便笺：账户 {account.bbs_uid} 树脂:{board.current_resin},未满足推送条件")


async def resin_check_sr(user_id: str, matcher: Matcher = None):
    """
    查看星铁实时便笺函数，并发送给用户任务执行消息。

    :param user_id: 用户QQ号
    :param matcher: 事件响应器
    """
    global has_checked
    user = _conf.users[user_id]
    for account in user.accounts.values():
        if account.enable_resin:
            has_checked[account.bbs_uid] = has_checked.get(account.bbs_uid,
                                                           {"stamina": False, "train_score": False,
                                                            "rogue_score": False})
        if account.enable_resin or matcher:
            starrail_board_status, board = await StarRail_board(account)
            if not starrail_board_status:
                if starrail_board_status.login_expired:
                    if matcher:
                        await matcher.send(f'⚠️账户 {account.bbs_uid} 登录失效，请重新登录')
                if starrail_board_status.no_starrail_account:
                    if matcher:
                        await matcher.send(f'⚠️账户 {account.bbs_uid} 没有绑定任何星铁账户，请绑定后再重试')
                    account.enable_resin = False
                    write_plugin_data()
                    continue
                if matcher:
                    await matcher.send(f'⚠️账户 {account.bbs_uid} 获取实时便笺请求失败，你可以手动前往App查看')
                continue
            if starrail_board_status.need_verify:
                if matcher:
                    await matcher.send('⚠️遇到验证码正在尝试绕过')
            msg = ''
            # 手动查询体力时，无需判断是否溢出
            if not matcher:
                # 体力溢出提醒
                if board.current_stamina == 180:
                    # 防止重复提醒
                    if has_checked[account.bbs_uid]['stamina']:
                        return
                    else:
                        has_checked[account.bbs_uid]['stamina'] = True
                        msg += '❕您的开拓力已经满啦\n'
                else:
                    has_checked[account.bbs_uid]['stamina'] = False
                # 每日实训状态提醒
                if board.current_train_score == board.max_train_score:
                    # 防止重复提醒
                    if has_checked[account.bbs_uid]['train_score']:
                        return
                    else:
                        has_checked[account.bbs_uid]['train_score'] = True
                        msg += '❕您的每日实训已完成\n'
                else:
                    has_checked[account.bbs_uid]['train_score'] = False
                # 每周模拟宇宙积分提醒
                if board.current_rogue_score == board.max_rogue_score:
                    # 防止重复提醒
                    if has_checked[account.bbs_uid]['rogue_score']:
                        return
                    else:
                        has_checked[account.bbs_uid]['rogue_score'] = True
                        msg += '❕您的模拟宇宙积分已经打满了\n\n'
                else:
                    has_checked[account.bbs_uid]['rogue_score'] = False
                    return
            msg += "❖星穹铁道实时便笺❖" \
                   f"\n⏳开拓力数量：{board.current_stamina} / 180" \
                   f"\n⏱开拓力{board.stamina_recover_text}" \
                   f"\n📒每日实训：{board.current_train_score} / {board.max_train_score}" \
                   f"\n📅每日委托：{board.accepted_expedition_num} / 4" \
                   f"\n🌌模拟宇宙：{board.current_rogue_score} / {board.max_rogue_score}"

            if matcher:
                await matcher.send(msg)
            else:
                if board.current_stamina >= account.user_stamina_threshold:
                    await send_private_msg(user_id=user_id, message=msg)
                else:
                    logger.info(f"崩铁实时便笺：账户 {account.bbs_uid} 开拓力:{board.current_stamina},未满足推送条件")


@scheduler.scheduled_job("cron", hour='0', minute='0', id="daily_goodImg_update")
def daily_update():
    """
    每日图片生成函数
    """
    logger.info(f"{_conf.preference.log_head}后台开始生成每日商品图片")
    threading.Thread(target=generate_image).start()


@scheduler.scheduled_job("cron",
                         hour=_conf.preference.plan_time.split(':')[0],
                         minute=_conf.preference.plan_time.split(':')[1],
                         id="daily_schedule")
async def daily_schedule():
    """
    自动米游币任务、游戏签到函数
    """
    # 随机延迟
    await asyncio.sleep(random.randint(0, 59))
    logger.info(f"{_conf.preference.log_head}开始执行每日自动任务")
    for qq in _conf.users:
        await perform_bbs_sign(user_id=qq)
        await perform_game_sign(user_id=qq)
    logger.info(f"{_conf.preference.log_head}每日自动任务执行完成")


@scheduler.scheduled_job("interval",
                         minutes=_conf.preference.resin_interval,
                         id="resin_check")
async def auto_resin_check():
    """
    自动查看实时便笺
    """
    for qq in _conf.users:
        await resin_check(user_id=qq)
        await resin_check_sr(user_id=qq)
