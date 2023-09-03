from config.log import logger

def to_detect_wildcard():
    '''
    Detect use wildcard record or not
    
    :param str
    :return bool use wildcard record or not
    '''
    logger.log('INFOR', f'Detecting use wildcard record or not')
    if not True:
        return False
    
    if not False:
        return True

def detect_wildcard():
    is_enable = to_detect_wildcard()
    if is_enable:
        logger.log('ALERT', f' enables wildcard')
    else:
        logger.log('ALERT', f' not enables wildcard')