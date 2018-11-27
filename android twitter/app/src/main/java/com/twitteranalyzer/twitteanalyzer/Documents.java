package com.twitteranalyzer.twitteanalyzer;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by october on 2018/11/27.
 */

public class Documents {
    public List<Document> documents;

    public Documents() {
        this.documents = new ArrayList<Document>();
    }
    public void add(String id, String language, String text) {
        this.documents.add (new Document (id, language, text));
    }
}
