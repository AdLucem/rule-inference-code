{-# LANGUAGE ScopedTypeVariables #-}

import qualified Data.ByteString.Lazy as BL
import Data.Csv
import qualified Data.Vector as V
import Data.List

data Token = Token {
  name :: String,
  startIndex :: Int,
  endIndex :: Int,
  hasSpace :: Int,
  posTag :: String,
  isNE :: Bool
                   } deriving (Show, Read, Eq)

data Rule = Rule {
  isInternal :: Bool,
  contextWindow :: Int,
  matrixLevel :: Int,
  sequence :: [String]
                 } deriving (Show, Read, Eq)

extractNEIndices :: [Token] -> [[Int]]
extractNEIndices corpus = extractNEHelper 0 False [] [] $ extractLevel 6 corpus []

extractNEHelper :: Int -> Bool -> [Int] -> [Int] -> [String] -> [[Int]]
extractNEHelper index False startIndexList endIndexList [] = [reverse startIndexList,reverse endIndexList]
extractNEHelper index True startIndexList endIndexList [] = [reverse startIndexList,reverse (index - 1 : endIndexList)]
extractNEHelper index False startIndexList endIndexList isNEList = case (read (head isNEList) :: Bool)  of
  False -> extractNEHelper (index+1) False startIndexList endIndexList (tail isNEList)
  True  -> extractNEHelper (index+1) True (index : startIndexList) endIndexList (tail isNEList)
extractNEHelper index True startIndexList endIndexList isNEList = case (read (head isNEList) :: Bool) of
  False -> extractNEHelper (index+1) False startIndexList ((index - 1) : endIndexList) (tail isNEList)
  True  -> extractNEHelper (index+1) True startIndexList endIndexList (tail isNEList)

extractLevel :: Int -> [Token] -> [String] -> [String]
extractLevel level [] acc = reverse acc
extractLevel level corpus acc = case level of
  1 -> extractLevel level (tail corpus) ((name (head corpus)) : acc)
  2 -> extractLevel level (tail corpus) ((show (startIndex (head corpus))) : acc)
  3 -> extractLevel level (tail corpus) ((show (endIndex (head corpus))) : acc)
  4 -> extractLevel level (tail corpus) ((show (hasSpace (head corpus))) : acc)
  5 -> extractLevel level (tail corpus) ((posTag (head corpus)) : acc)
  6 -> extractLevel level (tail corpus) ((show (isNE (head corpus))) : acc)

extractWindowHelper :: Int -> Int -> (Int -> Int -> Int -> Int) -> Int -> [String] -> [String] -> [String]
extractWindowHelper 0 offset op namedEntityIndex corpus window = reverse window
extractWindowHelper n offset op namedEntityIndex corpus window = if (op n offset namedEntityIndex) < (length corpus)
  then
  extractWindowHelper (n-1) offset op namedEntityIndex corpus ((corpus !! (op n offset namedEntityIndex)) : window)
  else
  reverse  window

isNamedEntity :: Int -> [Int] -> Bool
isNamedEntity index namedEntityIndexList =
  index `elem` namedEntityIndexList

extractWindows :: (Int -> Int -> Int -> Int) -> Int -> Int -> Int -> [[Int]] -> [String] -> [String] -> [[String]] -> [[String]]
extractWindows op index n offset nerIndexList [] corpus windowList = reverse windowList
extractWindows op index n offset nerIndexList levicorpus corpus windowList = if isNamedEntity index (nerIndexList !! 0)
  then
  extractWindows op (index + 1) n offset nerIndexList (tail levicorpus) corpus ((extractWindowHelper n offset op index corpus []) : windowList)
  else
  extractWindows op (index + 1) n offset nerIndexList (tail levicorpus) corpus windowList

sub :: Int -> Int -> Int -> Int
sub n offset namedEntityIndex = (namedEntityIndex - offset - n) 

main :: IO ()
main = let
  ans = show $ extractWindows sub 2 2 0 (extractNEIndices corpusList) (extractLevel 5 corpusList []) (extractLevel 5 corpusList []) [] 
  in putStrLn ans

corpusList :: [Token]
corpusList = [Token "Allylic" 0 7 1 "JJ" False,
  Token "Oxidation" 8 17 1 "NN" False,
  Token "Catalyzed" 18 27 1 "VBN" False,
  Token "by" 28 30 1 "IN" False,
  Token "Dirhodium(II)" 31 44 1 "NN" True,
  Token "Tetrakis[ε-cXaprolactamate]" 45 71 1 "NN" True,
  Token "of" 72 74 1 "IN" False,
  Token "tert-Butyldimethylsilyl-protected" 75 108 1 "JJ" True,
  Token "trans-Dehydroandrosterone" 109 134 1 "NN" True]
