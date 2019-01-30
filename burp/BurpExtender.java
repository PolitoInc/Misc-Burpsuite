package burp;

import java.awt.*;
import java.awt.event.*;
import java.net.*;
import java.util.*;
import java.io.*;
import java.applet.*;
import javax.swing.*;

public class BurpExtender implements IBurpExtender, IHttpListener, ITab, IScannerListener {

    public PrintWriter stdout;
    public IExtensionHelpers helper;
    public URL request_sound, param_sound, excellent;
    public JCheckBox requests, params, highseverity;

    @Override
    public void newScanIssue(IScanIssue issue) {
        String severity = issue.getSeverity();
        // play high severity sound if selected
        if (severity.equals("High") && this.highseverity.isSelected()) {
            Sound s = new Sound(this.excellent);
            new Thread(s).start();
        }
    }

    @Override
    public String getTabCaption() {
    	return "Sound Cues Options";
    }

    @Override
    public Component getUiComponent() {
    	JPanel panel = new JPanel();

    	this.requests = new JCheckBox("Requests Sound", true);
    	this.params = new JCheckBox("URL Params Sound", true);
        this.highseverity = new JCheckBox("High Severity Sound", true);

    	panel.setLayout(new FlowLayout());
    	panel.add(this.requests);
    	panel.add(this.params);
        panel.add(this.highseverity);

    	return panel;
    }
    
    @Override
    public void registerExtenderCallbacks(IBurpExtenderCallbacks callbacks)
    {

        // set our extension name
        callbacks.setExtensionName("Sound Effects");
        callbacks.registerHttpListener(this);
        callbacks.registerScannerListener(this);
        callbacks.addSuiteTab(this);

        this.helper = callbacks.getHelpers();

        // obtain our output and error streams
        PrintWriter stdout = new PrintWriter(callbacks.getStdout(), true);
        PrintWriter stderr = new PrintWriter(callbacks.getStderr(), true);
        this.stdout = stdout;

        InputStream param = null, request = null;

        this.param_sound = getClass().getClassLoader().getResource("assets/param.wav");
        this.request_sound = getClass().getClassLoader().getResource("assets/request.wav");
        this.excellent = getClass().getClassLoader().getResource("assets/excellent.wav");
    }

    @Override
    public void processHttpMessage(int toolFlag, boolean messageIsRequest, IHttpRequestResponse messageInfo) {
        if (messageIsRequest) {
            //play request sound if selected
            if (this.requests.isSelected()) {
            	Sound s = new Sound(this.request_sound);
            	new Thread(s).start();
            }
        } else {
            //play response sound
        }

        IRequestInfo req = this.helper.analyzeRequest(messageInfo);
        String url = req.getUrl().toString();
        // play params sound if selected
        if (url.contains("?") && this.params.isSelected()) {
            Sound s = new Sound(this.param_sound);
            new Thread(s).start();
        }
    }

    static class Sound implements Runnable {

        public AudioClip clip;

        public Sound(URL resource) {
            this.clip = Applet.newAudioClip(resource);
        }

        public void run() {
            this.clip.play();
        }
    }
}