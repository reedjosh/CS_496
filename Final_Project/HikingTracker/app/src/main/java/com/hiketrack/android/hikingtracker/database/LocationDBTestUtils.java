package com.hiketrack.android.hikingtracker.database;

import android.content.ContentValues;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.util.Log;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by jreed on 8/17/17.
 */

public class LocationDBTestUtils {

    private static final String logTag = "Joshua's LocationDBTestUtils:";

    public static void insertTestData(SQLiteDatabase db){
        if (db==null) return;
        List<ContentValues> dataList = new ArrayList<>();

        ContentValues cv = new ContentValues();
        cv.put(LocationDBContract.LocationDBEntry.COLUMN_LATITUDE, 122.4);
        cv.put(LocationDBContract.LocationDBEntry.COLUMN_LONGITUDE, 55.4);
        dataList.add(cv);

        cv = new ContentValues();
        cv.put(LocationDBContract.LocationDBEntry.COLUMN_LATITUDE, 102.4);
        cv.put(LocationDBContract.LocationDBEntry.COLUMN_LONGITUDE, 50.4);
        dataList.add(cv);

        cv = new ContentValues();
        cv.put(LocationDBContract.LocationDBEntry.COLUMN_LATITUDE, 12.4);
        cv.put(LocationDBContract.LocationDBEntry.COLUMN_LONGITUDE, 105.4);
        dataList.add(cv);

        db.beginTransaction();
        try{
            db.delete(LocationDBContract.LocationDBEntry.TABLE_NAME, null, null);

            for (ContentValues values: dataList) db.insert(LocationDBContract.LocationDBEntry.TABLE_NAME, null, values);
        } catch (SQLException ex){
            Log.i(logTag, "Database insertion error");
        }
        finally{
            db.endTransaction();
        }
    }
}
