package com.example.healthai;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class PaymentDetailsActivity extends AppCompatActivity {

    Button homepageButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_payment_details);
        homepageButton = findViewById(R.id.button_homepage);

        homepageButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent HomescreenActivityIntent = new Intent(PaymentDetailsActivity.this, HomescreenActivity.class);
                startActivity(HomescreenActivityIntent);
            }
        });

    }
}
