from pyspark import SparkConf, SparkContext
import sys
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.sql import SQLContext
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.ml.feature import StopWordsRemover
#import org.apache.spark.mllib.linalg.Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark.mllib.evaluation import MulticlassMetrics
def splitLines(line):
    line = line.split(", ")
    words = line[0]
    name = line[1]
    email = line[2]
    poi = line[3]
    return (name, email, poi, words)
	
def convertStrToInt(poi):
	if poi=='False':
		return 0
	else:
		return 1

def main(sc, sqlContext, inputPath, outputPath):
    
    # defaultParallelism - returns default level of parallelism defined on SparkContext (2 in our case)
    wordsRdd = sc.textFile(inputPath).repartition(sc.defaultParallelism * 20)
    dataRdd = wordsRdd.map(lambda line: splitLines(line))
    
     # define schema    
    schema = StructType([
    StructField('person', StringType(), False),
    StructField('email', StringType(), False),
    StructField('poi', StringType(), False),
    StructField('sentence', StringType(), False)
    ])
    
    dataFrameEnron =  sqlContext.createDataFrame(dataRdd, schema)   
    
    #print(dataFrameEnron.show())    
    
    # A tokenizer that converts the input string to lowercase and then splits it by white spaces.    
    tokenizer = Tokenizer(inputCol="sentence", outputCol="words")
    wordsData = tokenizer.transform(dataFrameEnron)
    
    #print(wordsData.select("sentence", "words").show())    
    
    # remove stop words i.e. words which do not contain important significance
    remover = StopWordsRemover(inputCol="words", outputCol="filtered")
    removedwordsData = remover.transform(wordsData)    
    
    #print(removedwordsData.select("words", "filtered").show())
    
    # perform TF using hashing. Maps a sequence of terms to their term frequencies using the hashing trick.
    hashingTF = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=100)
    featurizedData = hashingTF.transform(removedwordsData)
    
    # cache featurizedData for use in IDF
    featurizedData.cache()    
    
    # perform IDF
    # ignore terms which occur in less than a minimum number of documents.
    # In such cases, the IDF for these terms is set to 0.
    idf = IDF(minDocFreq=2, inputCol="rawFeatures", outputCol="features")
    idfModel = idf.fit(featurizedData)
    idfDataFrame = idfModel.transform(featurizedData)
    
    # unpersist featurizedData
    featurizedData.unpersist()
    
    # convert to LabeledPoint format to allow processing via mllib algorithms
    rescaledData = idfDataFrame.rdd
    rescaledDataLP=rescaledData.map(lambda row: LabeledPoint(convertStrToInt(row['poi']), row['features']) )
    
    # Split into Train, Test and Validation dataset
    split = [.9, .1]    
    trainData, testData = rescaledDataLP.randomSplit(split)
    
    # Train a DecisionTree model.
    # Empty categoricalFeaturesInfo indicates all features are continuous.
    model = DecisionTree.trainClassifier(trainData, numClasses=2, categoricalFeaturesInfo={}, impurity='gini', maxDepth=5, maxBins=32)						 

    # Evaluate model on test instances and compute test error
    predictions = model.predict(testData.map(lambda x: x.features))
    labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
    metrics = MulticlassMetrics(labelsAndPredictions)
    precision = metrics.precision()
    testErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(testData.count())
    
    output = []
    output.append('Test Error = ' + str(testErr)) 
    output.append('Precision =' + str(precision))
    output.append('Learned classification tree model:' + model.toDebugString())
    
    # Combining this data onto one node, I am sure it's safe to do so.    
    sc.parallelize(output).coalesce(1).saveAsTextFile(outputPath)   
    
    print(idfDataFrame.show())
   
if __name__ == "__main__":
    
    inputPath = sys.argv[1]
    outputPath = sys.argv[2]
    conf = SparkConf().setAppName('euler')
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    
    # call main method    
    main(sc, sqlContext, inputPath, outputPath)