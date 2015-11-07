from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

import requests
import thread
import time
from json import JSONEncoder

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS

clientID = ""
class EchoServerProtocol(WebSocketServerProtocol):

    def onMessage(self, payload, isBinary):
        zprava = self.message_data
        self.sendMessage("zprava_prijata: " + payload, isBinary)
        print zprava

        if zprava[0].startswith("REGID="):
            global clientID
            regid = zprava[0][6:] # REGID=APA91bEgXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXr3b-UyOoA-RmdBS_cGZsM'
            clientID = regid
            print clientID
            sendGCMnotification(clientID, title="WS spojeni navazano", message="Klient byl uspesne pripojen\n pres WebSocket na server!")


        def vyzadanaNotifikace(text):
            global clientID
            print "Vyzadana notifikace bude odeslana za 10s"
            print "clientID: " + clientID
            time.sleep(10)
            sendGCMnotification(clientID, title="Vyzadna notifikace", message=text)

        if zprava[0].startswith("N="):
            text = zprava[0][2:] # REGID=APA91bEgXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXr3b-UyOoA-RmdBS_cGZsM'
            print text
            thread.start_new_thread(vyzadanaNotifikace, (text, ))

    def onOpen(self):
        print("### opened ###")

    def onClose(self, wasClean, code, reason):
        print("### closed ###")


def sendGCMnotification(clientID, title, message):
    print "GCM send"

    if not clientID: # je prazdny
        print "clientID je prazdny, neni kam poslat notifikaci!"
        return

    # curl -X POST -H "Authorization: key=AIzXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXCYqU" -H "Content-Type: application/json" -d '{"registration_ids":["APA91bFpyYJb9PwXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX9phsDMFs1A9I4CF"],"priority":"high","data":{"message":"Testovaci zprava :-)","title":"Testovaci notifikace."}}' https://android.googleapis.com/gcm/send

    url = "https://android.googleapis.com/gcm/send"
    print url

    headers = { 'Authorization' : 'key=AIzXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXCYqU',
                'Content-Type' : 'application/json'
                }
    print headers

    #data = '{"registration_ids":["'+clientID+'"],"priority":"high","data":{"message":"Testovaci zprava :-)","title":"Testovaci notifikace."}}'

    data = JSONEncoder().encode({   # http://stackoverflow.com/a/13531266/1974494
        "priority" : "high",
        "data" : {
                "message" : message,
                "title" : title
        },
        "registration_ids" : [ clientID ]
    })
    print data

    try:
        r = requests.post(url, headers=headers, data=data)
        response = r.text
        response_code = r.status_code
        print "response= " + str(response)
        print "response_status_code= " + str(response_code)
    except Exception, e:
        return "WTF?"
    else:
        print "Prijata data: " + response


if __name__ == '__main__':

    sendGCMnotification(clientID, "Notifikace pri spusteni serveru", "text...")

    debug = True
    factory = WebSocketServerFactory(u"ws://192.168.0.50:9000",
                                     debug=debug,
                                     debugCodePaths=debug)

    factory.protocol = EchoServerProtocol
    factory.setProtocolOptions(allowHixie76=True)
    listenWS(factory)

    webdir = File(".")
    web = Site(webdir)
    reactor.listenTCP(9001, web)

    reactor.run()


