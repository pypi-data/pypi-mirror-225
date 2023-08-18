def keyword_finder(keyword_list, to_match):
    import pandas as pd 
    import numpy as np

    keywords = [str(x) for x in keyword_list if not pd.isna(x)]
    matches = []

    if type(to_match) == str:
        print("Stringo")
        from spacy.lang.en import English
        nlp = English()
        from spacy.matcher import PhraseMatcher
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

        ### Add the keywords
        patterns = [nlp.make_doc(text) for text in keywords]
        matcher.add('AI', patterns)

        stringo = nlp(to_match)

        matched_phrases = matcher(stringo)

        if len(matched_phrases) > 0:

            for match_id, start, end in matched_phrases:

                span = stringo[start:end]    

                matches.append(span.text)

            return list(set(matches))    
        
        else:
            return []

    elif type(to_match) == list:

        from spacy.lang.en import English
        nlp = English()
        from spacy.matcher import PhraseMatcher
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

        ### Add the keywords
        patterns = [nlp.make_doc(text) for text in keywords]
        matcher.add('AI', patterns)

        records = []

        for texto in to_match:

            internal_matches = []

            stringo = nlp(texto)

            matched_phrases = matcher(stringo)

            if len(matched_phrases) > 0:

                for match_id, start, end in matched_phrases:

                    span = stringo[start:end]    

                    internal_matches.append(span.text)
            else:
                internal_matches = np.nan

            record = {"Original": texto, "Keywords": internal_matches}

            records.append(record)
        
        cat = pd.DataFrame.from_records(records)

        if len(cat) > 0:
            return cat
        
        else:
            return []

    else:

        raise TypeError("Sorry, you can only pass a string or a list to match against")




def matcher(original=[], lookup=[], outname='Original', ngram_length=3, cutoff=0.8):
    import pandas as pd
    from tfidf_matcher.ngrams import ngrams
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.neighbors import NearestNeighbors

    k_matches=1

    # Enforce listtype, set to lower
    original = list(original)
    lookup = list(lookup)
    original_lower = [x.lower() for x in original]
    lookup_lower = [x.lower() for x in lookup]

    # Set ngram length for TfidfVectorizer callable
    def ngrams_user(string, n=ngram_length):
        return ngrams(string, n)

    # Generate Sparse TFIDF matrix from Lookup corpus
    vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams_user)
    tf_idf_lookup = vectorizer.fit_transform(lookup_lower)

    # Fit KNN model to sparse TFIDF matrix generated from Lookup
    nbrs = NearestNeighbors(n_neighbors=k_matches, n_jobs=-1, metric="cosine").fit(tf_idf_lookup)

    # Use nbrs model to obtain nearest matches in lookup dataset. Vectorize first.
    tf_idf_original = vectorizer.transform(original_lower)
    distances, lookup_indices = nbrs.kneighbors(tf_idf_original)

    # Extract top Match Score (which is just the distance to the nearest neighbour),
    # Original match item, and Lookup matches.
    original_name_list = []
    confidence_list = []
    index_list = []
    lookup_list = []
    print(len(lookup_indices))
    # i is 0:len(original), j is list of lists of matches
    for i, lookup_index in enumerate(lookup_indices):
        original_name = original[i]
        # lookup names in lookup list
        lookups = [lookup[index] for index in lookup_index]
        # transform distances to confidences and store
        confidence = [1 - round(dist, 2) for dist in distances[i]]
        original_name_list.append(original_name)
        # store index
        index_list.append(lookup_index)
        confidence_list.append(confidence)
        lookup_list.append(lookups)

    # Convert to df
    df_orig_name = pd.DataFrame(original_name_list, columns=[outname])

    df_lookups = pd.DataFrame(
        lookup_list, columns=["Match"]
    )
    df_confidence = pd.DataFrame(
        confidence_list,
        columns=["Match Confidence"],
    )

    # bind columns
    matches = pd.concat([df_orig_name, df_lookups, df_confidence], axis=1)

    # reorder columns | can be skipped
    lookup_cols = list(matches.columns.values)
    lookup_cols_reordered = [lookup_cols[0]]
    for i in range(1, k_matches + 1):
        lookup_cols_reordered.append(lookup_cols[i])
        lookup_cols_reordered.append(lookup_cols[i + k_matches])
        # lookup_cols_reordered.append(lookup_cols[i + 2 * k_matches])
    matches = matches[lookup_cols_reordered]

    matches = matches.loc[matches["Match Confidence"] > cutoff]
    matches.sort_values(by=["Match Confidence"], ascending=False, inplace=True)

    return matches