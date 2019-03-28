package com.example.djk16.nao;

public class robotinfo {
    private static robotinfo instance;

    public static robotinfo getInstance() {
        if (instance == null)
            instance = new robotinfo();
        return instance;
    }

    private robotinfo() {
    }

    private String ip;
    private String port;

    public String getIP() {
        return ip;
    }
    public String getPort() {
        return port;
    }

    public void setIP(String value) {
        this.ip = value;
    }
    public void setPort(String value) {
        this.port = value;
    }
}