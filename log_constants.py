# 通用常量
# 格式化时间
DATA_FORMAT = "%m/%d/%y %H:%M:%S:%f"
TIME_PATTERN = r'\[(\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}:\d{3})\]'

# 解析onUserJoined中的userId
log_message = "ChannelProxy::onUserJoined->onUserJoined(this:0x6f09d09700, userId:\"5\")"



# 关键字常量
# 版本号
KEY_VERSION = "Agora SDK ver"
# 日志完整性
KEY_INTEGRALITY = "API call to join"
# 重启编码器
KEY_RESET_CODEC = "resetCodec"
# 编码方式
KEY_ENCODE_MODE = "Init Succeeds, hw_encoder_accelerating: 1"
# 解码方式
KEY_DECODE_MODE = "Init Succeeds, hw_decoder_accelerating: 1"
# [rp]相关信息
KEY_RP = "\[rp\]"


# 创建引擎
KEY_ENGINE_CREATE = "RtcEngine::initializeEx"
# 销毁引擎
KEY_ENGINE_DESTROY = "RtcEngine::release:"


# 加入频道
KEY_JOIN_CHANNEL = "RtcEngine::joinChannel:"
# 离开频道
KEY_LEAVE_CHANNEL = "RtcEngine::leaveChannel:"
# 加入频道成功
KEY_JOIN_SUCCESS = "Proxy::onJoinChannelSuccess"


# enableLocalVideo
KEY_ENABLE_LOCAL_VIDEO = "RtcEngine::enableLocalVideo"
# enableLocalAudio
KEY_ENABLE_LOCAL_AUDIO = "RtcEngine::enableLocalAudio"
# enableAudio
KEY_ENABLE_AUDIO = "RtcEngine::enableAudio"
# enableVideo
KEY_ENABLE_VIDEO = "RtcEngine::enableVideo"
# disableAudio
KEY_DISABLE_AUDIO = "RtcEngine::disableAudio"
# disableVideo
KEY_DISABLE_VIDEO = "RtcEngine::disableVideo"


# muteLocalVideo
KEY_MUTE_LOCAL_VIDEO = "RtcConnectionImpl::muteLocalVideo"
# muteLocalAudio
KEY_MUTE_LOCAL_AUDIO = "RtcConnectionImpl::muteLocalAudio"
# muteRemoteVideo
KEY_MUTE_REMOTE_VIDEO = "RtcConnectionImpl::muteRemoteVideo"
# muteRemoteAudio
KEY_MUTE_REMOTE_AUDIO = "RtcConnectionImpl::muteRemoteAudio"


# screenShareRequestSuccess
KEY_REQ_SUCCESS = "onRequestSuccess"


# CALL_BACK
# ChannelProxy::onFirstRemoteAudioFrame
KEY_ON_FIRST_REMOTE_AUDIO = "ChannelProxy::onFirstRemoteAudioFrame"
# ChannelProxy::onFirstRemoteVideoFrame
KEY_ON_FIRST_REMOTE_VIDEO = "ChannelProxy::onFirstRemoteVideoFrame"
# ChannelProxy::onFirstRemoteAudioDecoded
KEY_ON_FIRST_REMOTE_AUDIO_DECODED ="ChannelProxy::onFirstRemoteAudioDecoded"
# ChannelProxy::onFirstRemoteVideoDecoded
KEY_ON_FIRST_REMOTE_VIDEO_DECODED ="ChannelProxy::onFirstRemoteVideoDecoded"
# ChannelProxy::onUserJoined
KEY_ON_USER_JOINED = "ChannelProxy::onUserJoined"


