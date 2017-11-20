package com.hiketrack.android.hikingtracker;

import android.content.Context;
import android.database.Cursor;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.hiketrack.android.hikingtracker.database.LocationDBContract.*;

/**
 * Created by jreed on 8/17/17.
 */

public class LocationListAdapter extends RecyclerView.Adapter<LocationListAdapter.LocationViewHolder>{

    private Cursor mCursor;
    private Context mContext;
    private String mLogTag = "Joshua's LocatAdapter";


    public LocationListAdapter(Context context, Cursor cursor) {
        mContext = context;
        mCursor = cursor;
    }


    @Override
    public LocationViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        LayoutInflater inflater = LayoutInflater.from(mContext);
        View itemView = inflater.inflate(R.layout.location_item, parent, false);
        return new LocationViewHolder(itemView);
    }


    @Override
    public void onBindViewHolder(LocationViewHolder holder, int position) {
        Log.i(mLogTag, "In bindViewHolder.");
        // Check that there's something at requested cursor position.
        if (!mCursor.moveToPosition(position)) return;

        // Get latitude, longitude, and id associated with the cursor's position.
        Float lat = mCursor.getFloat(mCursor.getColumnIndex(LocationDBEntry.COLUMN_LATITUDE));
        Float lon = mCursor.getFloat(mCursor.getColumnIndex(LocationDBEntry.COLUMN_LONGITUDE));

        long id = mCursor.getLong(mCursor.getColumnIndex(LocationDBEntry._ID));

        holder.latitudeTV.setText(String.format("%.2f", lat));
        holder.longitudeTV.setText(String.format("%.2f", lon));
        holder.itemView.setTag(id);
    }


    public void swapCursor(Cursor newCursor) {
        Log.i(mLogTag, String.format("In swap cursor. %d", newCursor.getCount()));
        if (mCursor != null) mCursor.close();
        mCursor = newCursor;
        if (newCursor != null) this.notifyDataSetChanged();
    }


    @Override
    public int getItemCount(){return mCursor.getCount();}


    public class LocationViewHolder extends RecyclerView.ViewHolder {

        TextView latitudeTV;
        TextView longitudeTV;

        public LocationViewHolder(View itemView){
            super(itemView);
            latitudeTV  = (TextView) itemView.findViewById(R.id.lat_tv);
            longitudeTV = (TextView) itemView.findViewById(R.id.lon_tv);
        }
    }
}
