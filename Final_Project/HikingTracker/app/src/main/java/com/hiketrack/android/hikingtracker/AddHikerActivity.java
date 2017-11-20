package com.hiketrack.android.hikingtracker;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class AddHikerActivity extends AppCompatActivity {

    private static final String mLogTag = "Create Hiker";
    // Http Stuffs
    MediaType JSON = MediaType.parse("application/json; charset=utf-8");
    private EditText mEtHikerName;
    private EditText mEtHikerWeight;
    private EditText mEtHikerHeight;
    private Button mBtnCreateHiker;
    private OkHttpClient mOkHttpClient = new OkHttpClient();
    private JSONObject mJSONObject = new JSONObject();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_hiker);

        /* * UI Stuffs * */
        mEtHikerName = (EditText) findViewById(R.id.etHikerName);
        mEtHikerHeight = (EditText) findViewById(R.id.etHeight);
        mEtHikerWeight = (EditText) findViewById(R.id.etHikerWeight);
        mBtnCreateHiker = (Button) findViewById(R.id.btnCreateHiker);

        onButtonClickListener();

    }

    // Turn UI input into JSON data for post.
    private void getUIInput(){
        try {
            mJSONObject.put("name", mEtHikerName.getText().toString());
            mJSONObject.put("weight", mEtHikerHeight.getText().toString());
            mJSONObject.put("height", mEtHikerWeight.getText().toString());
        } catch (JSONException ex) {
            ex.printStackTrace();
        }
    }


    private void postHiker() {
        RequestBody requestBody = RequestBody.create(JSON, mJSONObject.toString());
        Request request = new Request.Builder()
                .url("https://hiking-tracker-jreed.appspot.com/hikers")
                .post(requestBody)
                .build();
        mOkHttpClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                e.printStackTrace();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                String r = response.body().string();
                Log.i("Create", r);
            }
        });
    }




    private void onButtonClickListener() {
        mBtnCreateHiker.setOnClickListener(new View.OnClickListener() {
                                               @Override
                                               public void onClick(View v) {
                                                   getUIInput();
                                                   postHiker();
                                               }
                                           }
        );
    }

}



