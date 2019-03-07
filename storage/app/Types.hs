module Types where

data Token = Token {
  name :: String,
  posTag :: String,
  isNE :: Bool
                   } deriving (Show, Read, Eq)

data Rule = Rule {
  isInternal :: Bool,
  contextWindow :: Int,
  matrixLevel :: Int,
  sequence :: [String]
                 } deriving (Show, Read, Eq)
