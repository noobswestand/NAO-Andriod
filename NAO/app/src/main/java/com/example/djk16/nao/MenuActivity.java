package com.example.djk16.nao;

import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

public class MenuActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);

        Button bnt = (Button) findViewById(R.id.bnt_connect);


        String FILE = "ip.txt";
        //load here
        FileInputStream fis = null;
        try {
            fis = openFileInput(FILE);
            InputStreamReader isr = new InputStreamReader(fis);
            BufferedReader br =  new BufferedReader(isr);
            StringBuilder sb = new StringBuilder();
            String text;

            while((text = br.readLine()) != null)
            {
                sb.append(text);//.append("\n");
            }
            EditText txt = findViewById(R.id.txt_ip);
            txt.setText(sb.toString());

        }
        catch (FileNotFoundException e){
            e.printStackTrace();
        } catch (IOException e){
            e.printStackTrace();
        }
        finally{
            if(fis != null) {
                try {
                    fis.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }



        bnt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                EditText txt = (EditText) findViewById(R.id.txt_ip);
                String ip=txt.getText().toString();
                robotinfo.getInstance().setIP(ip);

                EditText txt2 = (EditText) findViewById(R.id.txt_port);
                String port=txt2.getText().toString();
                robotinfo.getInstance().setPort(port);

                Intent intent =new Intent(MenuActivity.this,ConnectingActivity.class);
                intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                startActivity(intent);

            }
        });

    }
}
