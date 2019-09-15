"""
This is the StructPy Frame testing suite. This uses pytest and logs information to `Unit Tests/Truss_pytest.log`. All functions beginning with `test_` are functions run by pytest, other functions aid in testing.

There are several example frames in .yaml files. These are file formatted to store structure information. They are used for the purpose of easily testing many known solutions.
"""

from pytest import approx
import yaml
import logging

logging.basicConfig(filename='Unit Tests/Frame_pytest.log',
					level=logging.INFO,
				    format='%(message)s')
logging.info(f'Running: {__name__}')

import StructPy.cross_sections as xs
import StructPy.structural_classes as sc
import StructPy.materials as ma
import StructPy.Frame as Frame
import numpy as np

def test_basic():
	xs1 = xs.generalSection(A=1, Ix=1)
	ma1 = ma.Custom(E=29000)
	
	f1 = Frame.Frame(cross=xs1, material=ma1)
	f1.addNode(0, 0, fixity='fixed')
	f1.addNode(10, 0)
	f1.addMember(0, 1)
	
	assert (f1.K == f1.members[0].k).all()
	assert (f1.K == f1.members[0].kglobal).all()

def test_Ex_6_2_5():
	"""
	Continuous Beam (Rajan, pg. 369)
	"""
	xs1 = xs.generalSection(A=0.01, Ix=0.0001)
	ma1 = ma.Custom(E=2*10**11)
	f1 = Frame.Frame(cross=xs1, material=ma1)
	
	# Nodes
	f1.addNode(0, 0, fixity='fixed')
	f1.addNode(2, 0, fixity='roller')
	f1.addNode(5, 0, fixity='roller')
	
	# Members
	f1.addMember(0, 1)
	f1.addMember(1, 2)
	# node, x, y, theta
	# 0
	# 1
	loading = np.array([0, -2000, -666.66667,
						0, -5000, 666.66667-1500,
						0, -3000, 1500])
	
	f1.directStiffness(loading)