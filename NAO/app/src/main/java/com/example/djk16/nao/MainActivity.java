package com.example.djk16.nao;

import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.URL;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final MainActivity _this=this;

        Button bnt=(Button) findViewById(R.id.bnt_hello);

        bnt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                EditText txt = (EditText) findViewById(R.id.txt_line);
                String line=txt.getText().toString();

                TextView txt2=findViewById(R.id.textView);
                txt2.setText(line);

                Say test = new Say(_this);
                test.execute(robotinfo.getInstance().getIP(),line);

            }
        });

    }

    private class Say extends AsyncTask<String, Void, String> {

        AppCompatActivity main;

        public Say(AppCompatActivity m) {
            main = m;
        }

        String text;


        @Override
        protected String doInBackground(String... params) {
            String ip = params[0];
            String line = params[1];
            int port = 5000;

            Socket socket;
            try {
                socket = new Socket();
                socket.connect(new InetSocketAddress(ip, port), 2000);
                DataOutputStream dOut = new DataOutputStream(socket.getOutputStream());


                dOut.writeByte(2);
                dOut.writeShort(line.length());
                dOut.writeChars(line);

                dOut.flush(); // Send off the data


                DataInputStream dIn = new DataInputStream(socket.getInputStream());
                byte messageType = dIn.readByte();
                int test = messageType;

                dOut.close();
                socket.close();

                if (test == 0) {
                    text = "Failed to connect to robot";
                } else {
                    text = "Connected";
                }

            } catch (Exception e) {
                text = "Failed to connect to service";
            }
            return text;
        }
    }
}
