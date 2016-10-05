#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file B2SComp.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
b2scomp_spec = ["implementation_id", "B2SComp", 
		 "type_name",         "B2SComp", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "VenderName", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class B2SComp
# @brief ModuleDescription
# 
# LEDRTCがShort型データによって点灯を制御しているため、Buttonユニットなどの二値制
#	御による点灯を可能にするための変換コンポーネント。True=1023、False=0として出力を
#	行う
# 
# InPort: BUTTONRTCなどのBoolean型出力をうけつける
#	OutPort: LEDRTCへの信号出力
# 
# 
class B2SComp(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		b_signal_arg = [None] * ((len(RTC._d_TimedBoolean) - 4) / 2)
		self._d_b_signal = RTC.TimedBoolean(*b_signal_arg)
		"""
		Boolean型データを受け取る
		 - Type: Boolean
		"""
		self._B_SignalIn = OpenRTM_aist.InPort("B_Signal", self._d_b_signal)
		
		#Change code run write() like ver.1.1.0
		#s_signal_arg = [None] * ((len(RTC._d_TimedShort) - 4) / 2)
		#self._d_s_signal = RTC.TimedShort(*s_signal_arg)
		self._d_s_signal = RTC.TimedShort(RTC.Time(0,0),0)
		
		"""
		Short型データを出力する
		 - Type: Short
		 - Number: 1
		"""
		self._S_SignalOut = OpenRTM_aist.OutPort("S_Signal", self._d_s_signal)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		
		# Set InPort buffers
		self.addInPort("B_Signal",self._B_SignalIn)
		
		# Set OutPort buffers
		self.addOutPort("S_Signal",self._S_SignalOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The activated action (Active state entry action)
	#	# former rtc_active_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	# 
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onActivated(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The deactivated action (Active state exit action)
	#	# former rtc_active_exit()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onDeactivated(self, ec_id):
	#
	#	return RTC.RTC_OK
	
		##
		#
		# The execution action that is invoked periodically
		# former rtc_active_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onExecute(self, ec_id):
		if(self._B_SignalIn.isNew()):
			
			self._d_b_signal = self._B_SignalIn.read()
			if(self._d_b_signal.data):
				self._d_s_signal.data = 1023
			else:
				self._d_s_signal.data = 0

		self._S_SignalOut.write()		
		print self._d_s_signal.data
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def B2SCompInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=b2scomp_spec)
    manager.registerFactory(profile,
                            B2SComp,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    B2SCompInit(manager)

    # Create a component
    comp = manager.createComponent("B2SComp")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

