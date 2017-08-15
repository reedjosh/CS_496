

package com.example.jreed.myapp;


import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.content.Intent;
import android.widget.EditText;
import android.widget.TextView;


public class MainActivity extends AppCompatActivity {

    private static Button button_1;
    private static Button button_2;
    private static Button button_3;
    private static Button button_4;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        onButtonClickListener();
    }

    public void onButtonClickListener() {
        button_1 = (Button) findViewById(R.id.button1);
        button_1.setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        Intent intent = new Intent("com.example.jreed.myapp.VerticalActivity");
                        startActivity(intent);
                    }
                }
        );
        button_2 = (Button) findViewById(R.id.button2);
        button_2.setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        Intent intent = new Intent("com.example.jreed.myapp.HorizontalActivity");
                        startActivity(intent);
                    }
                }
        );
        button_3 = (Button) findViewById(R.id.button3);
        button_3.setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        Intent intent = new Intent("com.example.jreed.myapp.GridActivity");
                        startActivity(intent);
                    }
                }
        );
        button_4 = (Button) findViewById(R.id.button4);
        button_4.setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        Intent intent = new Intent("com.example.jreed.myapp.RelativeActivity");
                        startActivity(intent);
                    }
                }
        );
    }

}
