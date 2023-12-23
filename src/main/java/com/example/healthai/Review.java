package com.example.healthai;

public class Review {
    private String reviewerName;
    private String reviewText;
    private double rating;

    public Review(String reviewerName, String reviewText, double rating) {
        this.reviewerName = reviewerName;
        this.reviewText = reviewText;
        this.rating = rating;
    }

    public String getReviewerName() {
        return reviewerName;
    }

    public String getReviewText() {
        return reviewText;
    }

    public double getRating() {
        return rating;
    }
}
