PythonWithWeka
=================

I write this one in order to use the various functions about NLP areas in Weka.

Weka is implemented by Java which is powerful in data mining, especially in NLP.

Asked to use the tf-idf and n-grams methods to make a Word2Vec model, I write a
simple demo here to show how to connect Python With Java practically.



HowToUseThis
-------------

Firstly, you should compile W2C.java with your JDK ,

and then you shold put the training datas in the format of Weka, like this way:
        -"training-source-root"
            -class1
                instance1.txt
                ,
                instance2.txt
                ,
                instance3.txt
                ...
            -class2
                instances1.txt
                ,
                instance2.txt
                ,
                instance3.txt
                ...
            -class
                isinstance
                ...

next, use W2C.class:

.. code:: java


    java W2C train <filename:training-source-root>

                   <filename:feature-transforming model>

                   <minGramCount :min number of the grams>

                   <maxGramCount :max number of the grams>

                   <WekaResults:results about dealing with the training datas>

Finished the tasks above, you've create a file like "Results.txt"(it's the input argument "WekaResults" of the W2C.class) in the workspace.

Then we using getPyW2CMd.py to make a model which can be used in Python Programs like gensim.models.Word2Vec.

.. code:: shell


    python getPyW2CMd.py <filename:training-source-root> <filename:WekaResults> <filename:PythonModel>

And then you create a file which is in Json format in fact. It's a Word2Vec model.

If the file PythonModel exists, you can use the Word2Vec Model in this way:

.. code:: python


    from PyWekaMake import W2C,makeX

    posEntities=['Publications_of_the_Astronomical_Society_of_the_Pacific,'
                'Geophysical_Journal_International',
                'Duke_Mathematical_Journal']
    negEntities=['Pease_Air_National_Guard_Base',
                'Jomsom_Airport',
                'Northern_Maine_Regional_Airport_at_Presque_Isle']
    model=W2C.load("PyWekaModel.json") # the name is only an example. You can define it by yourself.
    vecs1=[model[item] for item in posEntities]
    vecs2=[model[item] for item in negEntities]
    vecs1,vecs2=makeX(vecs1,vecs2)
