import pandas as pd
import numpy as np
import neattext.functions as nfx
# from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask,render_template,request

app = Flask(__name__)

def readData():
    df = pd.read_csv("courses-cleaned.csv")
    df.drop(columns=["Unnamed: 0"],inplace=True)
    return df

def getCleanTitle(df):
    # remove special character from course tag
    # df['tags'] = df['title'].apply(nfx.remove_stopwords)
    df['tags'] = df['title'].apply(nfx.remove_special_characters)
    df['tags'] = df['tags'].apply(lambda x:x.lower())
    # convert title case from upper to lower case
    df['title'] = df['title'].apply(lambda x:x.lower())
    return df

def getVector(df):
    cv = CountVectorizer(stop_words='english')
    vectors = cv.fit_transform(df['tags']).toarray()
    return vectors

def getSimilaritymat(vectors):
    similarity = cosine_similarity(vectors)
    return similarity


def recommend(df,title_name,similarity_mat,no_of_records):
    print("pass 1")
    course_index = pd.Series(df.index,index=df['title'])
    print("pass 2")
    index = course_index[title_name]
    print("pass 3")
    scores=list(enumerate(similarity_mat[index]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    selected_course_index = [i[0] for i in sorted_scores[1:]]
    selected_course_score = [i[1] for i in sorted_scores[1:]]
    rec_df = df.iloc[selected_course_index]
    rec_df['similarity_score'] = selected_course_score
    final_rec_courses=rec_df[['title', 'is_paid', 'price', 'course_cover_image', 'headline','instructor', 'course_url', 'ratings','similarity_score']]
    final_rec_courses = final_rec_courses.loc[final_rec_courses.similarity_score>0.5]

    return final_rec_courses

def extractfeatures(rec_df):
    course_title = list(rec_df['title'])
    course_price = list(rec_df['price'])
    course_cover_image = list(rec_df['course_cover_image'])
    course_instructor = list(rec_df['instructor'])
    course_url = list(rec_df['course_url'])
    course_rating = list(rec_df['ratings'])
    course_headline = list(rec_df['headline'])
    is_paid = list(rec_df['is_paid'])

    return course_title,course_price,course_cover_image,course_instructor,course_url,course_rating,course_headline,is_paid

def searchterm(term, df):
    result_df = df[df['tags'].str.contains(term)]
    top = result_df.sort_values(by='ratings', ascending=False)
    return top

@app.route('/', methods=['GET','POST'])
def index():
    
    
    if request.method=="GET":
        
        df_50 = pd.read_csv("top-50_cleaned.csv")
        df_50.drop(columns=['Unnamed: 0'],inplace=True)
        df_50 = df_50.sample(7)
        df_50['title'] = df_50['title'].apply(lambda x:x.lower())
        df_50['title'] = df_50['title'].apply(nfx.remove_special_characters)
        course_title = list(df_50['title'])
        course_price = list(df_50['price'])
        course_cover_image = list(df_50['course_cover_image'])
        course_instructor = list(df_50['instructor'])
        course_url = list(df_50['course_url'])
        course_rating = list(df_50['ratings'])
        course_headline = list(df_50['headline'])
        is_paid = list(df_50['is_paid'])

        dictmap = list(zip(course_title,course_price,course_cover_image,course_instructor,course_url,course_rating,course_headline,is_paid))

        return render_template('index.html', coursemap=dictmap, showtitle_50=True)
    
    if request.method=="POST":
        my_dict = request.form
        title_name = my_dict['course']

        try:
            
            df = readData()
            print("data read SUCCESS")
            df = getCleanTitle(df)
            print("data cleaned SUCCESS")
            vectors = getVector(df)
            print("get vectors SUCCESS")
            no_of_records = 10
            similarity_mat = getSimilaritymat(vectors)
            print("get sim_mat SUCCESS")
            rec_df = recommend(df,title_name,similarity_mat,no_of_records)
            course_title,course_price,course_cover_image,course_instructor,course_url,course_rating,course_headline,is_paid = extractfeatures(rec_df)

            dictmap = list(zip(course_title,course_price,course_cover_image,course_instructor,course_url,course_rating,course_headline,is_paid))

            if len(dictmap) != 0:
                return render_template('index.html', coursemap=dictmap, coursename=title_name, showtitle=True)

            else:
                return render_template('index.html', showerror=True, coursename=title_name)
        except:
            resultdf = searchterm(title_name, df)

            if resultdf.shape[0] > 10:
                resultdf = resultdf
                course_title,course_price,course_cover_image,course_instructor,course_url,course_rating,course_headline,is_paid = extractfeatures(resultdf)

                # coursemap = dict(zip(course_title, course_url))
                coursemap = list(zip(course_title,course_price,course_cover_image,course_instructor,course_url,course_rating,course_headline,is_paid))

                if len(coursemap) != 0:
                    return render_template('index.html', coursemap=coursemap, coursename=title_name, showtitle=True)
                else:
                    return render_template('index.html', showerror=True, coursename=title_name)
                
            else:
                course_title,course_price,course_cover_image,course_instructor,course_url,course_rating,course_headline,is_paid = extractfeatures(resultdf)

                # coursemap = dict(zip(course_title, course_url))
                coursemap = list(zip(course_title,course_price,course_cover_image,course_instructor,course_url,course_rating,course_headline,is_paid))

                if len(coursemap) != 0:
                    return render_template('index.html', coursemap=coursemap, coursename=title_name, showtitle=True)
                else:
                    return render_template('index.html', showerror=True, coursename=title_name)
    return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)