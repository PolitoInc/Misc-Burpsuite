# Polito Inc.
# Nathan McBride

from burp import IBurpExtender
from burp import IHttpListener

from burp import ITab
from javax import swing
from java.awt import Dimension
 
from urlparse import urlparse
 
class BurpExtender(IBurpExtender, ITab, IHttpListener):

    uris = []
    analyticData = {}
 
    def registerExtenderCallbacks(self, callbacks):
        # keep a reference to our callbacks object
        self._callbacks = callbacks
        # obtain an extension helpers object
        self._helpers = callbacks.getHelpers()
        # set out extension name
        self._callbacks.setExtensionName("Polito Inc. :: Request Analytics")
        

        
        # create out GUI
        self._jPanel = swing.JPanel()
        mainVerticalBox = swing.Box.createVerticalBox()

        descriptionHorizontalBox = swing.Box.createHorizontalBox()
        descriptionHorizontalBox.add(swing.JLabel("<html><br /><br />Request Analytics will track every request made through Burp and track how many times each 'file' appears in only uniqe URIs.<br />Only URIs included in scope will be analyzed.<br /><br /><br /></html>"))
        mainVerticalBox.add(descriptionHorizontalBox)

        controlsHorizontalBox = swing.Box.createHorizontalBox()
        displayAnalyticDataButton = swing.JButton('Display Analytic Data', actionPerformed=self.displayAnalyticData)
        controlsHorizontalBox.add(displayAnalyticDataButton)
        resetAnalyticDataButton = swing.JButton('Reset Analytic Data', actionPerformed=self.resetAnalyticData)
        controlsHorizontalBox.add(resetAnalyticDataButton)
        mainVerticalBox.add(controlsHorizontalBox)

        spacer1HorizontalBox = swing.Box.createHorizontalBox()
        spacer1HorizontalBox.add(swing.JLabel("<html><br /><br /><br /></html>"))
        mainVerticalBox.add(spacer1HorizontalBox)

        outputHorizontalBox = swing.Box.createHorizontalBox()
        self._outputTextArea = swing.JTextArea()
        self._outputTextArea.setEditable(False)
        outputTextArea = swing.JScrollPane(self._outputTextArea)
        outputTextArea.setPreferredSize(Dimension(250,300))
        outputHorizontalBox.add(outputTextArea)
        mainVerticalBox.add(outputHorizontalBox)
        
        self._jPanel.add(mainVerticalBox)



        # register ourselves as an HTTP listener
        self._callbacks.registerHttpListener(self)
        # add the custom tab to Burp's UI
        self._callbacks.addSuiteTab(self)

        return
 
    def processHttpMessage(self, toolFlag, messageIsRequest, currentRequest):
        # only process requests
        if not messageIsRequest:
            return
        
        # grab the url from the requestinfo object 
        requestInfo = self._helpers.analyzeRequest(currentRequest)
        url_obj = requestInfo.getUrl()

        # make sure the url is in scope
        if not self._callbacks.isInScope(url_obj):
            return

        url = str(url_obj)

        # remove the paramaters off of the url
        if '?' in url:
            u = url.split('?')[0]
        else:
            u = url

        # add the uris to our list
        if u not in self.uris:
            self.uris.append(u)

        return

    def getTabCaption(self):
        
        return "Request Analytics"
    
    def getUiComponent(self):
        
        return self._jPanel

    def displayAnalyticData(self, button):

        self.analyticData = {}
        
        for u in self.uris:

            # split the path and grab the last part
            path = urlparse(u).path
            path_parts = path.split('/')
            final_part = path_parts[len(path_parts) - 1]
            
            # add the final part to our dictionary
            if final_part in self.analyticData.keys():
                self.analyticData[final_part] = self.analyticData[final_part] + 1
            else:
                self.analyticData[final_part] = 1

        self._outputTextArea.setText("")

        if len(self.uris) <= 0:
            self._outputTextArea.append("There is no data to display.  Make sure a site is added to scope.")
            return

        analyticData_view = [ (v,k) for k,v in self.analyticData.iteritems() ]
        analyticData_view.sort(reverse=True)
        for v,k in analyticData_view:
            if k == '': k = '/'
            self._outputTextArea.append("%s: %d\n" % (k,v))
        self._outputTextArea.append(" \n")

        return

    def resetAnalyticData(self, button):
        self._outputTextArea.setText("")
        self.analyticData = {}
        self.uris = []
        self._outputTextArea.append("Analytic data has been reset.")

        return








