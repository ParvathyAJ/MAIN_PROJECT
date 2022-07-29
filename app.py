import random

from flask import Flask,request,render_template,session
from DBConnection import Db
import datetime
app = Flask(__name__)

app.secret_key="tocs"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/log')
def login():
    return render_template("login1.html")

@app.route('/login',methods=["post"])
def login1():
    db=Db()
    uname=request.form['textfield']
    pwd=request.form['textfield2']
    res=db.selectOne("select * from login where username='"+uname+"' and password='"+pwd+"'")
    if res is not None:
        lid=res['login_id']
        utype=res['user_type']
        session["lo"]="lin"
        session["lid"]=lid
        session["utype"]=utype
        if utype=="admin":
            return render_template("adminhome.html")
        else:
            return render_template("user/check_bacteria_classfn_using_cnn.html")
    else:
        return '<script>alert("Invalid User");window.location="/"</script>'


@app.route('/admin')
def admin():
    if session["lo"]=="lin":
        type = session["utype"]
        if type == 'admin':
            return render_template("adminhome.html")
        else:
            return login()
    else:
        return login()


@app.route('/user')
def user():
    if session["lo"]=="lin":
        type = session["utype"]
        if type == 'user':
            return render_template('userhome.html')
        else:
            return login()
    else:
        return login()

@app.route('/logout')
def logout():
    session["lo"]=" "
    return render_template('login1.html')

@app.route('/userreg')
def userreg():
    return render_template("userreg.html")

@app.route('/userreg1',methods=["post"])
def userreg1():
    db=Db()
    name=request.form['textfield']
    age=request.form['textfield2']
    place=request.form['textfield3']
    email=request.form['textfield5']
    phone=request.form['textfield4']
    pwd=request.form['textfieldp']
    cpwd=request.form['textfieldcp']
    if pwd==cpwd:
        res1=db.insert("insert into login values(null,'"+email+"','"+pwd+"','user')")
        res=db.insert("insert into users values(null,'"+name+"','"+age+"','"+place+"','"+email+"','"+phone+"','"+str(res1)+"')")
        return '<script>alert("Registration success");window.location="/"</script>'
    else:
        return '<script>alert("Your Passwords are mismatch");window.location="/"</script>'


########################## admin ########################################

@app.route('/addbacteria')
def addbacteria():
    if session["lo"] == "lin":
        return render_template("admin/add_bacteria_details.html")
    else:
        return login()

@app.route('/addbacteria1',methods=["post"])
def addbacteria1():
    if session["lo"] == "lin":
        db = Db()
        name = request.form['textfield']
        type = request.form['textfield2']
        details = request.form['textarea']
        ima1 = request.files['fileField']
        ima2 = request.files['fileField2']
        date1=datetime.datetime.now().strftime("imag1%Y%m%d-%H%M%S")
        date2=datetime.datetime.now().strftime("imag2%Y%m%d-%H%M%S")
        ima1.save(r"C:\Users\aj\Downloads\bacteria_classification\bacteria_classification\static\bacteria_pics"+date1+'.jpg')
        ima2.save(r"C:\Users\aj\Downloads\bacteria_classification\bacteria_classification\static\bacteria_pics"+date2+'.jpg')
        path1="/static/bacteria_pics/"+date1+'.jpg'
        path2="/static/bacteria_pics/"+date2+'.jpg'
        res = db.insert("insert into bacteria values(null,'" + name + "','" + type + "','" + str(path1) + "','" + str(path2) + "','"+details+"')")
        return '<script>alert("Details successfully inserted");window.location="/admin"</script>'
    else:
        return login()

@app.route('/viewcomplaint')
def viewcomplaint():
    if session["lo"] == "lin":
        db = Db()
        res=db.select("select * from complaints,users where complaints.login_id=users.login_id and complaints.reply='pending'")
        return render_template("admin/view_complaints.html",data=res)
    else:
        return login()

@app.route('/sentreply/<id>')
def sentreply(id):
    if session["lo"] == "lin":
        db = Db()
        res = db.selectOne("select * from complaints,users where complaints.login_id=users.login_id and complaints.cid='"+str(id)+"'")
        return render_template("admin/send_reply.html",data=res)
    else:
        return login()

@app.route('/sentreply1/<id>',methods=["post"])
def sentreply1(id):
    if session["lo"] == "lin":
        db=Db()
        reply=request.form['textarea']
        res=db.update("update complaints set reply='"+reply+"',r_date=curdate() where cid='"+str(id)+"'")
        return '<script>alert("Reply sent");window.location="/viewcomplaint"</script>'
    else:
        return login()

@app.route('/viewrating')
def viewrating():
    if session["lo"] == "lin":
        db = Db()
        res = db.select("select * from rating,users where users.login_id=rating.login_id")
        return render_template("admin/view_rating.html",data=res)
    else:
        return login()

@app.route('/view_search_history')
def view_search_history():
    if session["lo"] == "lin":
        db = Db()
        res = db.select("select * from history,users where history.login_id=users.login_id")
        return render_template("admin/view_search_history.html",data=res)
    else:
        return login()

@app.route('/view_users')
def view_users():
    if session["lo"] == "lin":
        db = Db()
        res = db.select("select * from users")
        return render_template("admin/view_users.html",data=res)
    else:
        return login()

@app.route('/deleteuser/<id>')
def deleteuser(id):
    if session["lo"] == "lin":
        db = Db()
        res = db.delete("delete from users where login_id='"+str(id)+"'")
        res1 = db.delete("delete from login where login_id='"+str(id)+"'")
        return '<script>alert("Deleted successfully");window.location="/view_users"</script>'
    else:
        return login()

@app.route('/dataset_training')
def dataset_training():
    if session["lo"] == "lin":
        return render_template("admin/dataset_training_using_cnn.html")
    else:
        return login()

@app.route('/dataset_training1',methods=["post"])
def dataset_training1():
    if session["lo"] == "lin":

        # ---------------------------------------------------------------------------------
        # Part 1 - Building the CNN

        # Importing the Keras libraries and packages
        from keras.engine.saving import load_model
        from keras.models import Sequential
        from keras.layers import Conv2D
        from keras.layers import MaxPooling2D
        from keras.layers import Flatten
        from keras.layers import Dense

        import tensorflow as tf

        # Initialising the CNN
        classifier = Sequential()

        # Step 1 - Convolution
        classifier.add(Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'))

        # Step 2 - Pooling
        classifier.add(MaxPooling2D(pool_size=(2, 2)))

        # Adding a second convolutional layer
        classifier.add(Conv2D(32, (3, 3), activation='relu'))
        classifier.add(MaxPooling2D(pool_size=(2, 2)))

        # Step 3 - Flattening
        classifier.add(Flatten())

        # Step 4 - Full connection
        classifier.add(Dense(units=128, activation='relu'))
        classifier.add(Dense(units=1, activation='sigmoid'))

        # Compiling the CNN
        classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        # Part 2 - Fitting the CNN to the images
        from keras.preprocessing.image import ImageDataGenerator

        train_datagen = ImageDataGenerator(rescale=1. / 255,
                                           shear_range=0.2,
                                           zoom_range=0.2,
                                           horizontal_flip=True)

        test_datagen = ImageDataGenerator(rescale=1. / 255)

        training_set = train_datagen.flow_from_directory('static/datasets',
                                                         target_size=(64, 64),
                                                         batch_size=32,
                                                         class_mode='binary')

        test_set = test_datagen.flow_from_directory('static/datasets',
                                                    target_size=(64, 64),
                                                    batch_size=32,
                                                    class_mode='binary')

        classifier.fit_generator(training_set,
                                 steps_per_epoch=8000,
                                 epochs=25,
                                 validation_data=test_set,
                                 validation_steps=2000)

        # classifier.fit_generator(training_set,
        #                          steps_per_epoch=8,
        #                          epochs=5,
        #                          validation_data=test_set,
        #                          validation_steps=2)
        classifier.save('static/model/model.h5')
        # ------------------------------------------------------------------------------------------------

        return '<script>alert(" Training Success ");window.location="/admin"</script>'
        # return '<script>alert(" Success ");</script>'
    else:
        return login()
################################# user ####################################

@app.route('/viewprof')
def viewprof():
    if session["lo"] == "lin":
        db = Db()
        uid = session["lid"]
        res = db.selectOne("select * from users where login_id='"+str(uid)+"'")
        return render_template("user/view_profile.html",data=res)
    else:
        return login()

@app.route('/editprof/<uid>',methods=["post"])
def editprof(uid):
    if session["lo"] == "lin":
        db = Db()
        res = db.selectOne("select * from users where login_id='"+str(uid)+"'")
        return render_template("user/edit_profile.html",data=res)
    else:
        return login()

@app.route('/updateprof/<id>',methods=["post"])
def updateprof(id):
    if session["lo"] == "lin":
        db = Db()
        # uid = session["lid"]
        name = request.form['textfield']
        age = request.form['textfield2']
        place = request.form['textfield3']
        email = request.form['textfield5']
        phone = request.form['textfield4']
        res = db.update("update users set name='"+name+"',age='"+age+"',place='"+place+"',email='"+email+"',phone='"+phone+"' where login_id='"+str(id)+"'")
        return '<script>alert("Successfully updated ");window.location="/viewprof"</script>'
    else:
        return login()

@app.route('/post_rating')
def post_rating():
    if session["lo"] == "lin":
        return render_template("user/post_rating.html")
    else:
        return login()

@app.route('/post_rating1',methods=["post"])
def post_rating1():
    if session["lo"] == "lin":
        db=Db()
        b1=request.form['button2']
        uid = session["lid"]

        db = Db()
        res = db.selectOne("select * from rating where login_id='" + str(uid) + "'")
        if res is not None:
            db = Db()
            db.update("update rating set r_value='"+str(b1)+"' where login_id='" + str(uid) + "' ")
        else:
            db = Db()
            # if b1=="1":
            db.insert("insert into rating values(null,'"+str(b1)+"','"+str(uid)+"')")
            # elif b1=="2":
            #     db.insert("insert into rating values(null,'2','"+str(uid)+"')")
            # elif b1=="3":
            #     db.insert("insert into rating values(null,'3','"+str(uid)+"')")
            # elif b1=="4":
            #     db.insert("insert into rating values(null,'4','"+str(uid)+"')")
            # else:
            #     db.insert("insert into rating values(null,'5','"+str(uid)+"')")
        return '<script>alert("Successfully added ");window.location="/user"</script>'
    else:
        return login()

@app.route('/sent_complaint')
def sent_complaint():
    if session["lo"] == "lin":
        return render_template("user/sent_complaint.html")
    else:
        return login()

#@app.route('/sent_complaint1',methods=["post"])
def sent_complaint1():
    if session["lo"] == "lin":
        db = Db()
        comp = request.form['textarea']
        uid = session["lid"]
        res = db.insert("insert into complaints values(null,'" + comp + "',curdate(),'pending',curdate(),'" + str(uid) + "')")
        return '<script>alert("Successfully added ");window.location="/viewcomp_reply"</script>'
    else:
        return login()




@app.route('/pesticide',methods=["post"])
def pesticide():
    if session["lo"] == "lin":
        db = Db()
        bact=request.form['select']
        pesticide = request.form['textarea']
        res = db.insert("insert into pesticides values(null,'" + bact + "','" + str(pesticide) + "')")
        return '<script>alert("Successfully added ");window.location="/viewpesticide"</script>'
    else:
        return login()



@app.route('/viewpesticide')
def viewpesticide():
    if session["lo"] == "lin":
        return render_template("admin/view pesticide.html")
    else:
        return login()



@app.route('/pesticide1',methods=['post'])
def pesticide1():
    if session["lo"] == "lin":
        return render_template("admin/add pesticide.html")
    else:
        return login()


@app.route('/viewcomp_reply')
def viewcomp_reply():
    if session["lo"] == "lin":
        db = Db()
        uid = session["lid"]
        res=db.select("select * from complaints,users where complaints.login_id=users.login_id and users.login_id='"+str(uid)+"'")
        return render_template("user/view_complaints_reply.html",data=res)
    else:
        return login()

@app.route('/view_bacteria_details')
def view_bacteria_details():
    if session["lo"] == "lin":
        db = Db()
        res = db.select("select * from bacteria")
        return render_template("user/view_bacteria_details.html",data=res)
    else:
        return login()

@app.route('/pesticides')
def pesticides():
    if session["lo"] == "lin":
        db = Db()
        res = db.select("SELECT * FROM `pesticides`")
        return render_template("user/view_bacteria_detail1s.html",data=res)
    else:
        return login()

@app.route('/check_bacteria')
def check_bacteria():
    session["lo"]="lin"
    if session["lo"] == "lin":
        return render_template("user/check_bacteria_classfn_using_cnn.html")
    else:
        return login()

@app.route('/check_bacteria1',methods=["post"])
def check_bacteria1():
    if session["lo"] == "lin":

        print("")

        from keras.engine.saving import load_model
        import numpy as np
        from keras.preprocessing import image

        picture = request.files['fileField']
        date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        path = "static/tested/" + date + ".jpg"
        picture.save(path)


        try:
            test_image = image.load_img(path , target_size=(64, 64))
            test_image = image.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis=0)

            try:
                # classifierLoad = load_model('static/model/model.h5')
                # result = classifierLoad.predict(test_image)
                from newcnn import predict
                #
                # result = classifier.predict(test_image)
                # training_set.class_indices
                prediction = "Can't predict Image"
                result=predict(path)
                print(result,"===============================")
                result=[result]
                sug=""
                print(result,"=======================================+++++++++++++++++++++++++++++++++++++++",type(result))
                if result[0][0] == 0:
                    prediction = 'Acinetobacter_baumanii'
                    sug="Acinetobacter baumannii is a Gram-negative bacillus that is aerobic, pleomorphic and non-motile. An opportunistic pathogen," \
                        " A. baumannii has a high incidence among immunocompromised individuals, particularly those who have experienced a prolonged (> 90 d) hospital stay."
                elif result[0][0] == 1:
                    prediction = 'Actinomyces_israeli'
                    sug = "Actinomyces israelii is a colonial bacterium which can be found as a commensal in the mouth and tonsillar crypts. It can cause a chronic suppurative infection, actinomycosis, which is characterized by multiple abscesses drained by sinus tracts." \
                          " Actinomycotic abscesses can be found in the liver, appendix, lung and neck."
                elif result[0][0] == 2:
                    prediction = 'Bacteroides_fragilis'
                    sug = "Bacteroides fragilis is a bacteria that is a common component of the human colon bacteria. It has involvement in causing disease in humans under certain conditions." \
                          " The human colon is lined by a mucosal barrier that protects body tissues from being invaded by the bacteria that inhabits the intestinal cavity."
                elif result[0][0] == 3:
                    prediction = 'Bifidobacterium_spp'
                    sug ="Bifidobacterium spp. are anaerobic, nonpathogenic, Gram-positive bacteria, commensal to the human gut that are a possible anticancer drug-delivery vehicle" \
                         "Bifidobacteria are a group of bacteria called probiotics that normally live in your intestines and stomach. They help your body perform essential functions such as digestion and staving off harmful bacteria."
                elif result[0][0] == 4:
                    prediction = 'Candida_albicans'
                    sug ="Candida albicans is the most common cause of genital yeast infections. Normally, a type of bacteria called Lactobacillus keeps the amount of Candida in the genital area under control." \
                         " However, when Lactobacillus levels are disrupted in some way, Candida can overgrow and cause an infection."
                elif result[0][0] == 5:
                    prediction = 'Clostridium_perfringens'
                    sug ="Clostridium perfringens bacteria are one of the most common causes of foodborne illness (food poisoning). CDC estimates these bacteria cause nearly 1 million illnesses in the United States every year." \
                         " C. perfringens can be found on raw meat and poultry, in the intestines of animals, and in the environment."
                elif result[0][0] == 6:
                    prediction = 'Enterococcus_faecalis'
                    sug ="Enterococcus faecalis – formerly classified as part of the group D Streptococcus system – is a Gram-positive, commensal bacterium inhabiting the gastrointestinal tracts of humans." \
                         " Like other species in the genus Enterococcus, E. faecalis is found in healthy humans and can be used as a probiotic."
                elif result[0][0] == 7:
                    prediction = 'Enterococcus_faecium'
                    sug ="Enterococcus faecium is a Gram-positive, gamma-hemolytic or non-hemolytic bacterium in the genus Enterococcus." \
                         " It can be commensal (innocuous, coexisting organism) in the gastrointestinal tract of humans and animals, but it may also be pathogenic, causing diseases such as neonatal meningitis or endocarditis."
                elif result[0][0]==8:
                    prediction = 'Escherichia_coli'
                    sug = "Escherichia coli (abbreviated as E. coli) are bacteria found in the environment, foods, and intestines of people and animals." \
                          " E. coli are a large and diverse group of bacteria. However, certain strains of E. coli can cause symptoms including diarrhea, stomach pain and cramps and low-grade fever"
                elif result[0][0] == 9:
                    prediction = 'Fusobacterium'
                    sug ="Fusobacterium species are anaerobic, elongated, gram-negative rods. There are multiple species of Fusobacterium, but the one most associated with human disease is F. necrophorum, a cause of periodontal disease, tonsillitis, peritonsillar abscess, and thrombophlebitis of the jugular vein (Lemierre syndrome)."
                elif result[0][0] == 10:
                    prediction = 'Lactobacillus_casei'
                    sug ="Lacticaseibacillus casei shirota is an organism that belongs to the largest genus in the family Lactobacillaceae, a lactic acid bacteria, that was previously classified as Lactobacillus casei-01." \
                         " This bacteria has been identified as facultatively anaerobic or microaerophilic, acid-tolerant, non-spore-forming bacteria"
                elif result[0][0] == 11:
                    prediction = 'Lactobacillus_crispatus'
                    sug ="Lactobacillus is an anaerobic, gram positive, rod shaped bacteria. Lactobacillus crispatus is beneficial bacteria found in the vaginal tract, intestinal regions, and gut flora. " \
                         "This species has the ability to produce numerous antimicrobial compounds and helps to maintain an acidic environment in its host"
                elif result[0][0] == 12:
                    prediction = 'Lactobacillus_delbrueckii'
                    sug ="Lactobacillus delbrueckii subsp. bulgaricus (until 2014 known as Lactobacillus bulgaricus) is one of several bacteria found in other naturally fermented products." \
                         " It is a Gram-positive rod, nonmotile, and does not form spore"
                elif result[0][0] == 13:
                    prediction = 'Lactobacillus_gasseri'
                    sug ="Lactobacillus gasseri is a strain of Lactobacillus, a genus of bacteria naturally found in the digestive and urinary tracts. The bacteria are thought to help the body by suppressing harmful bacteria. " \
                         "This process, in turn, enhances immune function and aids in digestion"
                elif result[0][0] == 14:
                    prediction = 'Lactobacillus_jehnsenii'
                    sug ="Lactobacillus jensenii is a normal inhabitant of the lower reproductive tract in healthy women. It is also found on the skins of grapes at the time of their harvest. L. jensenii is sometimes used in producing fermented foods"
                elif result[0][0] == 15:
                    prediction = 'Lactobacillus_johnsonii'
                    sug ="Johnsonii in milk can help thicken mucous membranes and reduce the risk of developing stomach ulcers caused by Helicobacter pylori. The effect of Lactobacillus on H. pylori has shown to have greater effect when the Lactobacillus species is present in a cultured form such as milk "
                elif result[0][0] == 16:
                    prediction = 'Lactobacillus_paracasei'
                    sug ="Paracasei helps to strengthen the intestinal barrier and improve absorption of nutrients from food. When taken in conjunction with other probiotic strains, it can promote intestinal epithelial cell growth and protect the intestinal barrier from chemicals and pathogens."
                elif result[0][0] == 17:
                    prediction = 'Lactobacillus_plantarum'
                    sug ="Lactobacillus plantarum is a Gram-positive, nonmotile, non-sporeforming bacterium. Although Lactobacillus spp. are usually recognized as catalase-negative, true catalase and manganese-containing pseudocatalase activities have been found, under special conditions, in a few strains of Lb. plantarum. Some strains also exhibit nitrate- and haematin-dependent nitrite reductases. Strains showing atypical characteristics for the genus Lactobacillus," \
                         " for example pseudocatalase activity, nitrate reduction, etc., have often been included in the Lb. plantarum species."
                elif result[0][0] == 18:
                    prediction = 'Lactobacillus_reuteri'
                    sug ="Lactobacillus reuteri (L. reuteri) is a well-studied probiotic bacterium that can colonize a large number of mammals. In humans, L. reuteri is found in different body sites, including the gastrointestinal tract, urinary tract, skin, and breast milk."
                elif result[0][0] == 19:
                    prediction = 'Lactobacillus_rhamnosus'
                    sug ="Rhamnosus is a type of bacteria found in your intestines. It belongs to the genus Lactobacillus, a type of bacteria that produce the enzyme lactase. This enzyme breaks down the sugar lactose — which is found in dairy — into lactic acid. Bacteria from this genus, such as L. rhamnosus, are considered probiotic."
                elif result[0][0] == 20:
                    prediction = 'Lactobacillus_salivarius'
                    sug ="As the main bacteria in our mouth, Lactobacillus salivarius is important for maintaining dental hygiene. It also plays a role in preventing intestinal diseases and supporting the immune system."
                elif result[0][0] == 21:
                    prediction = 'Listeria_monocytogenes'
                    sug ="Listeria monocytogenes (L. monocytogenes) is a species of pathogenic (disease-causing) bacteria that can be found in moist environments, soil, water, decaying vegetation and animals, and can survive and even grow under refrigeration and other food preservation measures"
                elif result[0][0] == 22:
                    prediction = 'Micrococcus_spp'
                    sug ="Micrococcus species are the predominant microorganisms found in raw milk drawn aseptically from the udder. They are the constituents of the natural microflora of teat skin and have also been isolated from soil, water, and dust." \
                         "Micrococci have occasionally been reported as the cause of pneumonia, meningitis associated with ventricular shunts, septic arthritis, bacteremia, peritonitis, endophthalmitis, CR-BSI and endocarditis."
                elif result[0][0] == 23:
                    prediction = 'Neisseria_gonorrhoeae'
                    sug ="Neisseria gonorrhoeae is a bacterial pathogen responsible for gonorrhoea and various sequelae that tend to occur when asymptomatic infection ascends within the genital tract or disseminates to distal tissues."
                elif result[0][0] == 24:
                    prediction = 'Porfyromonas_gingivalis'
                    sug ="Porphyromonas gingivalis is a Gram-negative oral anaerobe that is involved in the pathogenesis of periodontitis, an inflammatory disease that destroys the tissues supporting the tooth, eventually leading to tooth loss."
                elif result[0][0] == 25:
                    prediction = 'Propionibacterium_acnes'
                    sug ="Propionibacterium acnes is a gram-positive human skin commensal that prefers anaerobic growth conditions and is involved in the pathogenesis of acne (Kirschbaum and Kligman, 1963). Acne is one of the most common skin diseases, affecting more than 45 million individuals in the United States."
                elif result[0][0] == 26:
                    prediction = 'Proteus'
                    sug ="Proteus is a genus of Gram-negative bacteria. Proteus bacilli are widely distributed in nature as saprophytes, being found in decomposing animal matter, sewage, manure soil, the mammalian intestine, and human and animal feces. They are opportunistic pathogens, commonly responsible for urinary and septic infections, often nosocomial."
                elif result[0][0] == 27:
                    prediction = 'Pseudomonas_aeruginosa'
                    sug ="Pseudomonas aeruginosa is a common encapsulated, Gram-negative, strict aerobic (although can grow anaerobically in the presence of nitrate), Rod-shaped bacterium that can cause disease in plants and animals, including humans. A species of considerable medical importance, P. aeruginosa is a multidrug resistant pathogen recognized for its ubiquity, its intrinsically advanced antibiotic resistance mechanisms, and its association with serious illnesses – hospital-acquired infections such as ventilator-associated pneumonia and various sepsis syndromes."
                elif result[0][0] == 28:
                    prediction = 'Staphylococcus_aureus'
                    sug ="Staphylococcus aureus is a Gram-positive round-shaped bacterium, a member of the Bacillota, and is a usual member of the microbiota of the body, frequently found in the upper respiratory tract and on the skin."
                elif result[0][0] == 29:
                    prediction = 'Staphylococcus_epidermidis'
                    sug ="Staphylococcus epidermidis is a Gram-positive bacterium, and one of over 40 species belonging to the genus Staphylococcus. It is part of the normal human flora, typically the skin flora, and less commonly the mucosal flora and also found in marine sponges. It is a facultative anaerobic bacteria."
                elif result[0][0] == 30:
                    prediction = 'Staphylococcus_saprophiticus'
                    sug ="Staphylococcus saprophyticus is a Gram-positive bacterium that is a common cause of uncomplicated urinary tract infections, especially in young sexually active females. It is also responsible for complications including acute pyelonephritis, epididymitis, prostatitis, and urethritis."
                elif result[0][0] == 31:
                    prediction = 'Streptococcus_agalactiae'
                    sug ="Streptococcus agalactiae (also known as group B streptococcus or GBS) is a gram-positive coccus (round bacterium) with a tendency to form chains (as reflected by the genus name Streptococcus). It is a beta-hemolytic, catalase-negative, and facultative anaerobe." \
                         "In adults, S. agalactiae may cause meningitis or septicaemia as well as localized infections such as subcutaneous abscesses, urinary tract infection or arthritis"
                elif result[0][0] == 32:
                    prediction = 'Veionella'
                    sug ="Veillonella are Gram-negative bacteria (Gram stain pink) anaerobic cocci, unlike most Bacillota, which are Gram-positive bacteria. This bacterium is well known for its lactate fermenting abilities. It is a normal bacterium in the intestines and oral mucosa of mammals." \
                         "It is evident that oral Veillonella species are associated with oral biofilms, which cause many human oral infectious diseases, such as periodontal diseases and dental caries."

                # if result[0][0] == 1:
                #     prediction = 'Acinetobacter_baumanii'
                # elif result[0][0] == 2:
                #     prediction = 'Actinomyces_israeli'
                # elif result[0][0] == 3:
                #     prediction = 'Bacteroides_fragilis'
                # elif result[0][0] == 4:
                #     prediction = 'Bifidobacterium_spp'
                # elif result[0][0] == 5:
                #     prediction = 'Candida_albicans'
                # elif result[0][0] == 6:
                #     prediction = 'Clostridium_perfringens'
                # elif result[0][0] == 7:
                #     prediction = 'Enterococcus_faecalis'
                # elif result[0][0] == 8:
                #     prediction = 'Enterococcus_faecium'
                # elif result[0][0]==9:
                #     prediction = 'Escherichia_coli'
                # elif result[0][0] == 10:
                #     prediction = 'Fusobacterium'
                # elif result[0][0] == 11:
                #     prediction = 'Lactobacillus_casei'
                # elif result[0][0] == 12:
                #     prediction = 'Lactobacillus_crispatus'
                # elif result[0][0] == 13:
                #     prediction = 'Lactobacillus_delbrueckii'
                # elif result[0][0] == 14:
                #     prediction = 'Lactobacillus_gasseri'
                # elif result[0][0] == 15:
                #     prediction = 'Lactobacillus_jehnsenii'
                # elif result[0][0] == 16:
                #     prediction = 'Lactobacillus_johnsonii'
                # elif result[0][0] == 17:
                #     prediction = 'Lactobacillus_paracasei'
                # elif result[0][0] == 18:
                #     prediction = 'Lactobacillus_plantarum'
                # elif result[0][0] == 19:
                #     prediction = 'Lactobacillus_reuteri'
                # elif result[0][0] == 20:
                #     prediction = 'Lactobacillus_rhamnosus'
                # elif result[0][0] == 21:
                #     prediction = 'Lactobacillus_salivarius'
                # elif result[0][0] == 22:
                #     prediction = 'Listeria_monocytogenes'
                # elif result[0][0] == 23:
                #     prediction = 'Micrococcus_spp'
                # elif result[0][0] == 24:
                #     prediction = 'Neisseria_gonorrhoeae'
                # elif result[0][0] == 25:
                #     prediction = 'Porfyromonas_gingivalis'
                # elif result[0][0] == 26:
                #     prediction = 'Propionibacterium_acnes'
                # elif result[0][0] == 27:
                #     prediction = 'Proteus'
                # elif result[0][0] == 28:
                #     prediction = 'Pseudomonas_aeruginosa'
                # elif result[0][0] == 29:
                #     prediction = 'Staphylococcus_aureus'
                # elif result[0][0] == 30:
                #     prediction = 'Staphylococcus_epidermidis'
                # elif result[0][0] == 31:
                #     prediction = 'Staphylococcus_saprophiticus'
                # elif result[0][0] == 32:
                #     prediction = 'Streptococcus_agalactiae'
                # elif result[0][0] == 33:
                #     prediction = 'Veionella'


                db = Db()
                print(prediction)
                # res = db.select("select * from pesticides where bacteria='"+str(prediction)+"'")
                res=""
                print("result---" + sug)
                return render_template("user/result.html",val=res,bacti=prediction,s=sug)

                # QMessageBox.about(self, "Result", prediction + "")
            except Exception as e:
                print("Error======",e)

        except Exception as e:
            print("Error222======",e)
            # QMessageBox.about(self, "Warning", "        Try Again        ")
            print("---")

        return render_template("user/result.html", val=res)
    else:
        return login()




@app.route('/sechpesticide',methods=["post"])
def sechpesticide():
    if session["lo"] == "lin":
        db = Db()
        bact=request.form['select']
        res = db.select("SELECT * FROM `pesticides` WHERE `bacteria`='"+bact+"'")
        print(res)
        return render_template("admin/view pesticide.html",val=res,b=bact)
    else:
        return login()




@app.route('/deletepesticide/<id>')
def deletepesticide(id):
    if session["lo"] == "lin":
        db = Db()
        res = db.delete("delete from pesticides where pid='"+str(id)+"'")
        return '<script>alert("Deleted successfully");window.location="/viewpesticide"</script>'
    else:
        return login()



if __name__ == '__main__':
    app.run()
