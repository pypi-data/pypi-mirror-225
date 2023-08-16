import logging


# Create a custom logger
def _buildLogger():

    _logger = logging.getLogger(__name__)

    logging.root.setLevel(logging.NOTSET)

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('./bsdm.log')
    c_handler.setLevel(logging.NOTSET)
    f_handler.setLevel(logging.ERROR)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    _logger.addHandler(c_handler)
    _logger.addHandler(f_handler)

    return _logger

LOGGER = _buildLogger()