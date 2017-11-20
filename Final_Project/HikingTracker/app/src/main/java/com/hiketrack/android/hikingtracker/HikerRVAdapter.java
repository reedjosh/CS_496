package com.hiketrack.android.hikingtracker;

import android.content.Context;
import android.database.Cursor;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by jreed on 8/18/17.
 */

public class HikerRVAdapter extends RecyclerView.Adapter<HikerRVAdapter.HikerViewHolder> {


    private List<Hiker> mHikerList;
    private Context mContext;
    private String mLogTag = "Joshua's HikerAdapter";


    public HikerRVAdapter(Context context, List<Hiker> hikerList) {
        mContext = context;
        mHikerList = hikerList;
    }


    @Override
    public HikerViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        LayoutInflater inflater = LayoutInflater.from(mContext);
        View itemView = inflater.inflate(R.layout.hiker_item, parent, false);
        return new HikerViewHolder(itemView);
    }


    @Override
    public void onBindViewHolder(HikerViewHolder holder, int position) {
        Log.i(mLogTag, "In bindViewHolder.");
        // Check that there's something at requested hikerLists position.
        if (position > mHikerList.size()) return;

        // Get latitude, longitude, and id associated with the cursor's position.
        Hiker hiker = mHikerList.get(position);
        if (hiker == null) return;
        Log.i("aTag", hiker.toString());
        int height = hiker.height;
        int weight = hiker.weight;
        String name = hiker.name;
        String id = hiker.id;

        Log.i("aTag", String.valueOf(height));
        holder.nameTV.setText(name);
        holder.heightTV.setText(String.valueOf(height));
        holder.weightTV.setText(String.valueOf(weight));
        holder.itemView.setTag(id);
    }


    //public void swapCursor(Cursor newCursor) {
    //    Log.i(mLogTag, String.format("In swap cursor. %d", newCursor.getCount()));
    //    if (mHikerList != null) mHikerList.close();
    //    mHikerList = newCursor;
    //    if (newCursor != null) this.notifyDataSetChanged();
    //}


    @Override
    public int getItemCount() {
        return mHikerList.size();
    }


    public class HikerViewHolder extends RecyclerView.ViewHolder {

        TextView nameTV;
        TextView heightTV;
        TextView weightTV;

        public HikerViewHolder(View itemView) {
            super(itemView);
            nameTV = (TextView) itemView.findViewById(R.id.tvName);
            heightTV = (TextView) itemView.findViewById(R.id.tvHeight);
            weightTV = (TextView) itemView.findViewById(R.id.tvWeight);
        }
    }
}
