FeatureSelection On Existed Gram2Vec Model
======

to do feature selection on  <model>.json.

- <model>.jsom
	
.. code:: json

	["<entity1>": [[<keyNum , N-Gram Index>],[<keyValue , TFIDF>]]
	...
	]

for instance:

- `test.json <https://github.com/thautwarm/NLPWorks/tree/master/201705/FeatureSelectionOnGram2VecExistedModel/test.json>`_


The Gram2Vector Model is in form of sparse features.

This Program is to:
	
- use weka for java API to do feature selection on plural existed Gram2Vec model.
- to show how convenient when use Kotlin instead of Java on some specific Project in the real world. 


HowToUseThis
-------------

Firstly, set corresponding working directory. 

Then(optinal), compile the program:

.. code:: shell
	
	kotlinc FeatureSelection.kt -include-runtime -cp ./lib/weka.jar -d Selector.jar

Next, write a config file in ".json" like:

.. code:: JSON
	
	// config.json

	[
 	{"jarRunFileName":"javaRun.bat",
  	 "JSONFileName":"test.json",
  	 "to_ArffFileName":"testone",
     "selectFeatureNum":"100"}
	]

Finally, run this project:

.. code:: shell
	
	python dicttake.py config.json

then you get 3 new files here:

.. code:: PlainText
	
	testone_corr.json
	testone_entropy.json
	testone_relief.json

As specific suffix suggests, the new models are decomposed(reduced) by following methods:

.. code:: PlainText	
		
	Correlation
	Entropy
	Relief(I don't know what it means in Weka, just like I don't know until now, that "entropy" means "infoGain"  )





