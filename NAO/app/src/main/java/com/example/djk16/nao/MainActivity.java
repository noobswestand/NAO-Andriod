package com.example.djk16.nao;

import android.app.Activity;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView txt_ip=findViewById(R.id.txt_ip);
        txt_ip.setText(robotinfo.getInstance().getIP()+":"+robotinfo.getInstance().getPort());

    }

    public void gotoSay(View v){
        Intent intent =new Intent(MainActivity.this,SayActivity.class);
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(intent);
    }

    public void gotoPosture(View v){
        Intent intent =new Intent(MainActivity.this,PostureActivity.class);
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(intent);
    }

    public void gotoBehavoir(View v){
        Intent intent =new Intent(MainActivity.this,BehavoirActivity.class);
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(intent);
    }
}
