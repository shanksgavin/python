--
-- Generated by DB Solo 4.1.1 on Thu Sep 26 13:19:55 EDT 2013
-- This script will modify the SOURCE database to be in sync with the destination database
-- Source: [omsprod_inland_20130926] [inland_20130926] [public]
-- Destination: [wiregrass 2.2.0.74] [wiregrass_2_2_0_74] [public]
-- 


--
-- settings
-- 

INSERT INTO public.settings (setting_name, 
                             setting_id, 
                             description, 
                             setting_value, 
                             type_info, 
                             category)
                             VALUES 
                            ('enable_beta_modules', 
                             -1, 
                             'Enable beta features.', 
                             'True', 
                             'boolean', 
                             'OMS');
INSERT INTO public.settings (setting_name, 
                             setting_id, 
                             description, 
                             setting_value, 
                             type_info, 
                             category)
                             VALUES 
                            ('interface_error_notification_ivr_enabled', 
                             -1, 
                             'Interface Error Notification for IVR Enabled', 
                             'True', 
                             'boolean', 
                             'Integration');
INSERT INTO public.settings (setting_name, 
                             setting_id, 
                             description, 
                             setting_value, 
                             type_info, 
                             category)
                             VALUES 
                            ('interface_error_notification_ivr_errorlevel', 
                             -1, 
                             'Interface Error for IVR Error Level Notification', 
                             'DEBUG', 
                             'text', 
                             'Integration');
INSERT INTO public.settings (setting_name, 
                             setting_id, 
                             description, 
                             setting_value, 
                             type_info, 
                             category)
                             VALUES 
                            ('interface_error_notification_service_link_enabled', 
                             -1, 
                             '', 
                             'True', 
                             'boolean', 
                             'OMS');
INSERT INTO public.settings (setting_name, 
                             setting_id, 
                             description, 
                             setting_value, 
                             type_info, 
                             category)
                             VALUES 
                            ('interface_error_notification_service_link_errorlevel', 
                             -1, 
                             '', 
                             'DEBUG', 
                             'text', 
                             'OMS');
INSERT INTO public.settings (setting_name, 
                             setting_id, 
                             description, 
                             setting_value, 
                             type_info, 
                             category)
                             VALUES 
                            ('interface_error_notifications_disabled', 
                             -1, 
                             '', 
                             'False', 
                             'boolean', 
                             'OMS');
INSERT INTO public.settings (setting_name, 
                             setting_id, 
                             description, 
                             setting_value, 
                             type_info, 
                             category)
                             VALUES 
                            ('scada_combine_phase_time', 
                             61, 
                             '', 
                             '120000', 
                             'integer', 
                             'Integration');
INSERT INTO public.settings (setting_name, 
                             setting_id, 
                             description, 
                             setting_value, 
                             type_info, 
                             category)
                             VALUES 
                            ('scada_default_cause', 
                             62, 
                             '', 
                             'Equipment', 
                             'text', 
                             'Integration');
INSERT INTO public.settings (setting_name, 
                             setting_id, 
                             description, 
                             setting_value, 
                             type_info, 
                             category)
                             VALUES 
                            ('scada_restore_cases', 
                             63, 
                             '', 
                             'True', 
                             'boolean', 
                             'Integration');
INSERT INTO public.settings (setting_name, 
                             setting_id, 
                             description, 
                             setting_value, 
                             type_info, 
                             category)
                             VALUES 
                            ('upn_call_sync_enabled', 
                             0, 
                             'Activates/Enables UPN(CIS) Call Sync', 
                             'False', 
                             'boolean', 
                             'Integration');
INSERT INTO public.settings (setting_name, 
                             setting_id, 
                             description, 
                             setting_value, 
                             type_info, 
                             category)
                             VALUES 
                            ('upn_call_sync_in_oms', 
                             0, 
                             '', 
                             'False', 
                             'boolean', 
                             'Integration');
INSERT INTO public.settings (setting_name, 
                             setting_id, 
                             description, 
                             setting_value, 
                             type_info, 
                             category)
                             VALUES 
                            ('upn_call_sync_in_upn', 
                             0, 
                             '', 
                             'False', 
                             'boolean', 
                             'Integration');
INSERT INTO public.settings (setting_name, 
                             setting_id, 
                             description, 
                             setting_value, 
                             type_info, 
                             category)
                             VALUES 
                            ('upn_call_sync_interval', 
                             0, 
                             '', 
                             '60', 
                             'integer', 
                             'Integration');

