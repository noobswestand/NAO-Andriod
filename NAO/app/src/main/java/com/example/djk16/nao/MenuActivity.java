package com.example.djk16.nao;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class MenuActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);

        Button bnt = (Button) findViewById(R.id.bnt_connect);

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
