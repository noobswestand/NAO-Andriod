package com.example.djk16.nao;

import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;

public class ConnectingActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_connecting);

        TestConnect test = new TestConnect(this);
        //test.execute("10.0.2.2");
        test.execute(robotinfo.getInstance().getIP());
    }

    private class TestConnect extends AsyncTask<String, Void, String> {

        AppCompatActivity main;
        public TestConnect(AppCompatActivity m){
            main=m;
        }
        String text;


        @Override
        protected String doInBackground(String... params) {
            String ip = params[0];
            int port=5000;

            Socket socket;
            try {
                socket = new Socket();
                socket.connect(new InetSocketAddress(ip,port),2000);
                DataOutputStream dOut = new DataOutputStream(socket.getOutputStream());


                dOut.writeByte(1);
                dOut.writeShort(robotinfo.getInstance().getIP().length());
                dOut.writeChars(robotinfo.getInstance().getIP());
                dOut.writeShort(robotinfo.getInstance().getPort().length());
                dOut.writeChars(robotinfo.getInstance().getPort());
                dOut.flush(); // Send off the data


                DataInputStream dIn = new DataInputStream(socket.getInputStream());
                byte messageType = dIn.readByte();
                int test=messageType;

                dOut.close();
                socket.close();

                if (test==0){
                    text="Failed to connect to robot";
                }else{
                    text="Connected";
                }

            } catch (Exception e) {
                text="Failed to connect to service";
            }
            return text;
        }

        @Override
        protected void onPostExecute(final String s) {
            if (text=="Connected"){
                Intent intent =new Intent(ConnectingActivity.this,MainActivity.class);
                intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                startActivity(intent);
            }else {
                TextView txt = main.findViewById(R.id.txt_connect);
                txt.setText(text);

                ProgressBar pgb=main.findViewById(R.id.progressBar);
                pgb.setVisibility(View.GONE);

                Button bnt=main.findViewById(R.id.bnt_back);
                bnt.setVisibility(View.VISIBLE);

                bnt.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {

                        Intent intent =new Intent(ConnectingActivity.this,MenuActivity.class);
                        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                        startActivity(intent);

                    }
                });


            }
        }

    }

}




