package com.example.orbital.lto.chatapp;

import java.util.Random;

import android.support.v7.app.ActionBarActivity;
import android.support.v7.app.ActionBar;
import android.support.v4.app.Fragment;
import android.text.Html;
import android.annotation.SuppressLint;
import android.app.*;
import android.content.*;
import android.os.Build;
import android.os.Bundle;
import android.view.*;
import android.webkit.*;
import android.widget.*;

public class MainActivity extends ActionBarActivity implements ActionBar.OnNavigationListener {

	class mobileScriptInterface {
		Context mContext;
		/**
		 * 
		 */
		public mobileScriptInterface(Context c) {
			mContext = c;
		}
		
		/** Obtaining chat message */
		@JavascriptInterface
		public void getMsg(final String m){
			runOnUiThread(new Runnable(){
	            public void run(){
	            	EditText txt= (EditText) findViewById(R.id.chatBox);
	            	String temp = m.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "\"").replace("&#39;", "'");
	    			txt.append(temp+"\n");
	            }

	        });
		}

	}
	
    /**
     * The serialization (saved instance state) Bundle key representing the
     * current dropdown position.
     */
    private static final String STATE_SELECTED_NAVIGATION_ITEM = "selected_navigation_item";
    
    private String _ROOMID = "";

    public static String random() {
        Random generator = new Random();
        String temp = "";
        for (int i = 0; i < 5; i++){
            temp = temp + generator.nextInt(5);
        }
        return temp;
    }
    
    @SuppressLint("SetJavaScriptEnabled") private void buildDialog(Context c){
    	AlertDialog.Builder alertDialogBuilder = new AlertDialog.Builder(
				c);
 
			// set title
    		AlertDialog alert = null;
			alertDialogBuilder.setTitle("Server Address");
			
			final EditText intxt = new EditText(this);
			
			final WebView web = (WebView) findViewById(R.id.web); 
        	
	        web.getSettings().setJavaScriptEnabled(true);
	        web.setEnabled(true);
	        web.addJavascriptInterface(new mobileScriptInterface(this), "Android");
	        final String Id = "mobile"+random();
	        web.setWebViewClient(new WebViewClient());
	        
	        
	        Button btn = (Button) findViewById(R.id.sendBtn);
	        btn.setOnClickListener(new Button.OnClickListener() {
	            public void onClick(View v) {
	                EditText intxt = (EditText) findViewById(R.id.inputBox);
	                String message = intxt.getText().toString();
	                intxt.setText("");
	                EditText chattxt = (EditText) findViewById(R.id.chatBox);
	                chattxt.append("I say: "+message+"\n");
	                web.loadUrl("javascript:sendMessage(\""+message+"\")");
	            }
	        });
			// set dialog message
			alert = alertDialogBuilder
				.setView(intxt)
				.setMessage("Input the server ip and port")
				.setCancelable(false)
				.setPositiveButton("Done",new DialogInterface.OnClickListener() {
					public void onClick(DialogInterface dialog,int id) {
						String value = intxt.getText().toString();
						_ROOMID = value;
						web.loadUrl(getString(R.string.chatWebClient)+_ROOMID+"&clientID="+Id);
					}
				  }).create();
			alert.show();
    	
    }
    
    @SuppressLint("SetJavaScriptEnabled") @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.fragment_main);
        buildDialog(this);
        
        
    }
    
    @Override
    public void onRestoreInstanceState(Bundle savedInstanceState) {
        // Restore the previously serialized current dropdown position.
        if (savedInstanceState.containsKey(STATE_SELECTED_NAVIGATION_ITEM)) {
            getSupportActionBar().setSelectedNavigationItem(
                    savedInstanceState.getInt(STATE_SELECTED_NAVIGATION_ITEM));
        }
    }

    @Override
    public void onSaveInstanceState(Bundle outState) {
        // Serialize the current dropdown position.
        outState.putInt(STATE_SELECTED_NAVIGATION_ITEM,
                getSupportActionBar().getSelectedNavigationIndex());
    }

    /**
     * A placeholder fragment containing a simple view.
     */
    public static class PlaceholderFragment extends Fragment {
        /**
         * The fragment argument representing the section number for this
         * fragment.
         */
        private static final String ARG_SECTION_NUMBER = "section_number";

        /**
         * Returns a new instance of this fragment for the given section
         * number.
         */
        public static PlaceholderFragment newInstance(int sectionNumber) {
            PlaceholderFragment fragment = new PlaceholderFragment();
            Bundle args = new Bundle();
            args.putInt(ARG_SECTION_NUMBER, sectionNumber);
            fragment.setArguments(args);
            return fragment;
        }

        public PlaceholderFragment() {
        }

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                Bundle savedInstanceState) {
            View rootView = inflater.inflate(R.layout.fragment_main, container, false);
            return rootView;
        }
    }

	@Override
	public boolean onNavigationItemSelected(int arg0, long arg1) {
		// TODO Auto-generated method stub
		return false;
	}

}