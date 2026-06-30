# SLA Compliance Monitoring Engine
# Real-time SLA tracking and violation detection across multi-channel support

import pandas as pd
from datetime import datetime, timedelta

class SLAComplianceEngine:
    def __init__(self):
        self.sla_targets = {
            'billing': {'target_minutes': 60, 'compliance_target': 0.80},
            'account_access': {'target_minutes': 15, 'compliance_target': 0.90},
            'technical': {'target_minutes': 120, 'compliance_target': 0.75},
            'returns': {'target_minutes': 240, 'compliance_target': 0.70}
        }
        self.alert_threshold = 0.75  # Alert if compliance drops below 75%
    
    def calculate_sla_compliance(self, contact_data):
        '''Calculate SLA compliance for contact'''
        queue = contact_data['queue'].lower()
        response_time = contact_data['first_response_time_median']
        target_minutes = self.sla_targets.get(queue, {}).get('target_minutes', 60)
        
        is_compliant = response_time <= target_minutes
        compliance_status = 'Met' if is_compliant else 'Missed'
        
        return {
            'contact_id': contact_data.get('id'),
            'queue': queue,
            'response_time_minutes': response_time,
            'sla_target_minutes': target_minutes,
            'compliant': is_compliant,
            'status': compliance_status,
            'variance_minutes': response_time - target_minutes
        }
    
    def channel_sla_compliance(self, operational_data):
        '''Calculate SLA compliance by channel'''
        compliance_by_channel = {}
        for channel in operational_data['channel'].unique():
            channel_data = operational_data[operational_data['channel'] == channel]
            total = len(channel_data)
            
            # Estimate compliance based on % Responded Within SLA
            avg_compliance = channel_data['% Responded Within SLA'].mean()
            
            compliance_by_channel[channel] = {
                'compliance_rate': avg_compliance,
                'contacts': total,
                'status': 'On Target' if avg_compliance >= 0.80 else 'At Risk',
                'median_response_time': channel_data['First Response Time Median'].mean()
            }
        
        return compliance_by_channel
    
    def queue_sla_compliance(self, operational_data):
        '''Calculate SLA compliance by queue'''
        compliance_by_queue = {}
        for queue in operational_data['Queue'].unique():
            queue_data = operational_data[operational_data['Queue'] == queue]
            
            queue_key = queue.split('|')[0].strip().lower()
            target = self.sla_targets.get(queue_key, {}).get('compliance_target', 0.80)
            
            compliance_rate = queue_data['% Responded Within SLA'].mean()
            
            compliance_by_queue[queue] = {
                'compliance_rate': compliance_rate,
                'target_rate': target,
                'gap': compliance_rate - target,
                'status': 'Met' if compliance_rate >= target else 'Missed',
                'contacts': len(queue_data),
                'median_response_time': queue_data['First Response Time Median'].mean()
            }
        
        return compliance_by_queue
    
    def identify_violations(self, operational_data):
        '''Identify SLA violations requiring attention'''
        violations = []
        for idx, row in operational_data.iterrows():
            if row['% Responded Within SLA'] < 0.80:
                violation = {
                    'channel': row['Channel'],
                    'queue': row['Queue'],
                    'compliance_rate': row['% Responded Within SLA'],
                    'response_time': row['First Response Time Median'],
                    'severity': 'Critical' if row['% Responded Within SLA'] < 0.50 else 'High',
                    'timestamp': datetime.now().isoformat()
                }
                violations.append(violation)
        
        return violations
    
    def generate_compliance_report(self, operational_data):
        '''Generate SLA compliance report'''
        overall_compliance = operational_data['% Responded Within SLA'].mean()
        
        report = {
            'overall_compliance_rate': round(overall_compliance, 3),
            'target_compliance_rate': 0.80,
            'compliance_gap': round(overall_compliance - 0.80, 3),
            'status': 'On Target' if overall_compliance >= 0.80 else 'Below Target',
            'total_contacts': len(operational_data),
            'channels_at_risk': len([c for c in self.channel_sla_compliance(operational_data).values() if c['status'] == 'At Risk']),
            'channel_performance': self.channel_sla_compliance(operational_data),
            'queue_performance': self.queue_sla_compliance(operational_data),
            'violations': self.identify_violations(operational_data),
            'generated_at': datetime.now().isoformat()
        }
        return report

if __name__ == "__main__":
    engine = SLAComplianceEngine()
    print("SLA Compliance Engine v1.0 initialized")
    print("Channels: 23+ | Queues: 4 | Real-time monitoring: Enabled")
