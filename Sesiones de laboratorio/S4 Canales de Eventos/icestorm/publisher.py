#!/usr/bin/python3

import sys
import Ice
import IceStorm
Ice.loadSlice('./Printer.ice')
import Example


class Publisher(Ice.Application):
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            print("property {} not set".format(key))
            return None

        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, argv):
        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            print('Invalid proxy')
            return 2

        topic_name = "PrinterTopic"
        try:
            topic = topic_mgr.create(topic_name)
        except IceStorm.TopicExists:
            topic = topic_mgr.retrieve(topic_name)

        publisher = topic.getPublisher()
        printer = Example.PrinterPrx.uncheckedCast(publisher)

        print("publishing 10 'Hello World' events")
        for i in range(10):
            printer.write("Hello World %s!" % i)

        return 0


sys.exit(Publisher().main(sys.argv))
