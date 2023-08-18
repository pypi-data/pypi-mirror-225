import logging
from urllib.parse import urlparse


def tenant_extractor(origin: str, x_tenant_id: str, default_tenant: str = 'public'):
    """
    Function to extract tenant from Origin/Header or assign default
    :param origin:
    :param x_tenant_id:
    :param default_tenant:
    :return:
    """
    subdomain = None
    logging.info("Starting to check subdomain.")
    if origin_name := urlparse(origin).hostname if origin else None:
        logging.info("Origin exists in the request. Checking hostname.")
        split = origin_name.split('.')
        subdomain = split[0] if len(split) > 0 else None
    elif x_tenant_id and not subdomain:
        logging.info("Origin doesn't exist. Checking Header for 'X-Tenant-ID'.")
        subdomain = x_tenant_id
    else:
        logging.info("'X-Tenant-ID' doesn't exist also, assigning default value.")
        subdomain = default_tenant

    return subdomain
