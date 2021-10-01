package com.catalystmedia.traffic

import android.content.Intent
import android.graphics.Color
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.speech.tts.TextToSpeech
import android.util.Log
import androidx.annotation.RequiresApi
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ValueEventListener
import kotlinx.android.synthetic.main.activity_main.*
import java.util.*

class MainActivity : AppCompatActivity(),TextToSpeech.OnInitListener {

    lateinit var tts:TextToSpeech

    @RequiresApi(Build.VERSION_CODES.R)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        window.decorView.windowInsetsController!!.hide(
            android.view.WindowInsets.Type.statusBars())
        updateData()
        tts = TextToSpeech(this, this)
    }


    private fun updateData() {
        FirebaseDatabase.getInstance().reference.child("server").child("traffic-data").child("roadData")
            .child("currentStatus").addValueEventListener(object : ValueEventListener {
                override fun onDataChange(snapshot: DataSnapshot) {
                    if(snapshot.exists()){
                        var data = snapshot.value.toString()
                        tv_best.text = "Best Route is $data"

                        tts!!.speak("Best Route is $data", TextToSpeech.QUEUE_FLUSH, null,"")


                        if(data == "A"){
                            iv_direction.setImageResource(R.drawable.ic_left)
                            iv_best_route.setImageResource(R.drawable.route_1)
                        }
                        else if (data == "B"){
                            iv_direction.setImageResource(R.drawable.ic_right)
                            iv_best_route.setImageResource(R.drawable.route_2)
                        }
                        else{
                            iv_direction.setImageResource(R.drawable.ic_up)
                            iv_best_route.setImageResource(R.drawable.route_3)
                        }

                    }
                }

                override fun onCancelled(error: DatabaseError) {
                    TODO("Not yet implemented")
                }
            })

        FirebaseDatabase.getInstance().reference.child("server").child("traffic-data").child("roadData")
            .child("carsFeed1").addValueEventListener(object : ValueEventListener {
                override fun onDataChange(snapshot: DataSnapshot) {
                    if(snapshot.exists()){
                        var data = snapshot.value.toString()
                        tv_car1.text = data
                        Handler(Looper.getMainLooper()).postDelayed({
                            tv_car1.setTextColor(Color.parseColor("#BBBBBB"))
                        }, 2000)
                        tv_car1.setTextColor(Color.parseColor("#00C845"))

                    }
                }

                override fun onCancelled(error: DatabaseError) {
                    TODO("Not yet implemented")
                }
            })

        FirebaseDatabase.getInstance().reference.child("server").child("traffic-data").child("roadData")
            .child("carsFeed2").addValueEventListener(object : ValueEventListener {
                override fun onDataChange(snapshot: DataSnapshot) {
                    if(snapshot.exists()){
                        var data = snapshot.value.toString()
                        tv_car2.text = data
                        Handler(Looper.getMainLooper()).postDelayed({
                            tv_car2.setTextColor(Color.parseColor("#BBBBBB"))
                        }, 2000)
                        tv_car2.setTextColor(Color.parseColor("#00C845"))

                    }
                }

                override fun onCancelled(error: DatabaseError) {
                    TODO("Not yet implemented")
                }
            })
    }

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            // set US English as language for tts
            val result = tts!!.setLanguage(Locale.US)

            if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                Log.e("TTS","The Language specified is not supported!")
            } else {

            }

        } else {
            Log.e("TTS", "Initilization Failed!")
        }
    }
    public override fun onDestroy() {
        // Shutdown TTS
        if (tts != null) {
            tts!!.stop()
            tts!!.shutdown()
        }
        super.onDestroy()
    }
}