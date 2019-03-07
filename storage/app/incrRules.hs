{-# LANGUAGE ScopedTypeVariables #-}

import qualified Data.ByteString.Lazy as BL
import Data.Csv
import qualified Data.Vector as V
import Data.List

import Types
import Corpus

extractNEIndices :: [Token] -> [[Int]]
extractNEIndices corpus = extractNEHelper 0 False [] [] $ extractLevel 3 corpus []

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
  2 -> extractLevel level (tail corpus) ((posTag (head corpus)) : acc)
  3 -> extractLevel level (tail corpus) ((show (isNE (head corpus))) : acc)

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
  ans = show $ extractWindows sub 2 2 0 (extractNEIndices corpusList) (extractLevel 2 corpusList []) (extractLevel 2 corpusList []) [] 
  in putStrLn ans
