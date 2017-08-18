package com.example.android.location_sq.database;

import android.provider.BaseColumns;

/**
 * Created by jreed on 8/17/17.
 */

public class LocationDBContract {
    public static final class LocationDBEntry implements BaseColumns {
        public static final String TABLE_NAME = "Locations";
        public static final String COLUMN_LATITUDE = "latitude";
        public static final String COLUMN_LONGITUDE = "longitude";
        public static final String COLUMN_TIMESTAMP = "timestamp";
    }
}
