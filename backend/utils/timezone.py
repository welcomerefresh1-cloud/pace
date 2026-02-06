from datetime import datetime, timezone, timedelta

# GMT+8 timezone (Philippine Standard Time)
GMT8 = timezone(timedelta(hours=8))


def get_current_time_gmt8() -> datetime:
    """Get current time in GMT+8 timezone"""
    return datetime.now(GMT8)


__all__ = ['GMT8', 'get_current_time_gmt8']
