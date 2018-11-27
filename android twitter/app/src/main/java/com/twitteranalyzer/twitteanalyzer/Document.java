package com.twitteranalyzer.twitteanalyzer;

/**
 * Created by october on 2018/11/27.
 */

public class Document {
    public String id, language, text;

    public Document(String id, String language, String text){
        this.id = id;
        this.language = language;
        this.text = text;
    }
}
