package com.example.android.myapplication;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;

import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;


public class MainActivity extends Activity  {

    // UI Elements.
    Button mBtnLogin,mBtnCancel;
    EditText mEtUsername, mEtPassword;

    // Login attempt counter.
    private static int mCounter = 3;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mBtnLogin = (Button)findViewById(R.id.btnLogin);
        mEtUsername = (EditText)findViewById(R.id.etUsername);
        mEtPassword = (EditText)findViewById(R.id.etUsername);

        mBtnCancel = (Button)findViewById(R.id.btnCancel);

        mBtnLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(mEtUsername.getText().toString().equals("admin") &&
                        mEtPassword.getText().toString().equals("password")) {
                    Toast.makeText(getApplicationContext(), "Redirecting...",Toast.LENGTH_SHORT).show();
                }else{
                    Toast.makeText(getApplicationContext(), "Wrong Credentials",Toast.LENGTH_SHORT).show();
                    if (counter == 0)mBtnLogin.setEnabled(false);
                }
            }
        });

        mBtnCancel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
    }
}
