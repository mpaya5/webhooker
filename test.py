import pandas as pd
import numpy as np
from function import actualizar_csv, fractals, start
import csv, requests, json
from pymongo import MongoClient
from urls import urls

#if ((short > long) & (long > middle)) or ((middle > short) & (short > long)) or ((long > short) & (short > middle)) or((middle > long) & (long > short)):