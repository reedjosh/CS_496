package com.hiketrack.android.hikingtracker;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.helper.ItemTouchHelper;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

/**
 * Created by jreed on 8/18/17.
 */

public class MainActivity extends AppCompatActivity implements Callback  {


    private List<Hiker> mHikerList = new ArrayList<>();
    private RecyclerView mHikerRV;
    private HikerRVAdapter mAdapter;
    private JSONObject mJSONObject = new JSONObject();
    private OkHttpClient mOkHttpClient = new OkHttpClient();
    private Button mBtnCreateNew;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_hikers);

        // Set create new button to load create new user profile
        mBtnCreateNew = (Button) findViewById(R.id.btnNewHiker);
        mBtnCreateNew.setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        Intent intent = new Intent("android.intent.action.AddHikerActivity");
                        startActivity(intent);
                    }
                }
        );

        Request request = new Request.Builder()
                .url("https://hiking-tracker-jreed.appspot.com/hikers")
                .build();

        mOkHttpClient.newCall(request).enqueue(MainActivity.this);
                /* * Setup swipe left right to delete location. * */
        /* This uses an item touch helper attached to the locationRecyclerView */
        /* This touch helper is largely inspired by Udacity's course on android development, and I just
        /* see much need to change stuff. Just so ya all know!
         */
        new ItemTouchHelper(new ItemTouchHelper.SimpleCallback(0, ItemTouchHelper.LEFT | ItemTouchHelper.RIGHT) {
            // onMove override is required, but not needed.
            @Override
            public boolean onMove(RecyclerView recyclerView, RecyclerView.ViewHolder viewHolder, RecyclerView.ViewHolder target) {
                return false;
            }
            // Get the tag of the item being swiped which corresponds to the ID of the location
            // in the database then delete the item from the database using the ID. Then update the
            // recycler view.
            @Override
            public void onSwiped(RecyclerView.ViewHolder viewHolder, int swipeDir) {
                String id = (String) viewHolder.itemView.getTag();
                deleteHiker(id); // The view should auto update.
            }
        }).attachToRecyclerView(mHikerRV);
    }

    private void deleteHiker(String id) {
        Request request = new Request.Builder()
                .url("https://hiking-tracker-jreed.appspot.com/hikers" + id)
                .delete()
                .build();
        mOkHttpClient.newCall(request).enqueue(MainActivity.this);

    }

    @Override
    public void onFailure(Call call, IOException e) {
        e.printStackTrace();
    }

    @Override
    public void onResponse(Call call, Response response) throws IOException {
        String r = response.body().string();
        try {
            JSONArray hikers = new JSONObject(r).getJSONArray("hikers");
            for (int i = 0; i < hikers.length(); i++) {
                JSONObject jsonHikerData = hikers.getJSONObject(i);
                Hiker hikerData = new Hiker();
                hikerData.name = jsonHikerData.getString("name");
                hikerData.id = jsonHikerData.getString("id");
                hikerData.height = jsonHikerData.getInt("height");
                hikerData.weight = jsonHikerData.getInt("weight");
                mHikerList.add(hikerData);
            }
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    mHikerRV = (RecyclerView) findViewById(R.id.rvHikers);
                    mAdapter = new HikerRVAdapter(MainActivity.this, mHikerList);
                    mHikerRV.setAdapter(mAdapter);
                    mHikerRV.setLayoutManager(new LinearLayoutManager(MainActivity.this));
                }
            });

        } catch (JSONException ex) {
            ex.printStackTrace();
        }
        Log.i("Create", r);
    }

}

//RecyclerView hikersRV = new RecyclerView();
//hikersRV = (RecyclerView) this.findViewById(R.id.locationsListView);
//hikerRVAdapter = new HikerRVAdapter(this, locationCursor);
//hikersRV.setAdapter(hikerRVAdapter);
//hikersRV.setLayoutManager(new LinearLayoutManager(this));

