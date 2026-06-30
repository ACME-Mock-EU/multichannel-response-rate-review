# Channel Performance Dashboard
# Real-time visibility into multi-channel support metrics and KPIs

import pandas as pd
from datetime import datetime

class ChannelPerformanceDashboard:
    def __init__(self):
        self.kpi_thresholds = {
            'sla_compliance': 0.80,
            'csat_score': 4.2,
            'abandon_rate': 0.03,
            'reopen_rate': 0.05,
            'escalation_rate': 0.05
        }
    
    def executive_summary(self, operational_data):
        '''Executive-level performance summary'''
        summary = {
            'total_channels': operational_data['Channel'].nunique(),
            'total_contacts': operational_data['Incoming Contacts'].sum(),
            'unique_customers': operational_data['Unique Customers'].sum(),
            'avg_response_time_median': operational_data['First Response Time Median'].mean(),
            'overall_sla_compliance': operational_data['% Responded Within SLA'].mean(),
            'avg_csat_score': operational_data['CSAT Score'].mean(),
            'avg_abandon_rate': operational_data['Abandon Rate'].mean(),
            'avg_escalation_rate': operational_data['Escalation Rate'].mean(),
            'health_status': self._calculate_health_status(operational_data),
            'generated_at': datetime.now().isoformat()
        }
        return summary
    
    def channel_performance_table(self, operational_data):
        '''Detailed performance by channel'''
        performance = []
        for channel in operational_data['Channel'].unique():
            channel_data = operational_data[operational_data['Channel'] == channel]
            
            perf = {
                'channel': channel,
                'contacts': int(channel_data['Incoming Contacts'].sum()),
                'customers': int(channel_data['Unique Customers'].sum()),
                'response_time_median': round(channel_data['First Response Time Median'].mean(), 1),
                'response_time_p90': round(channel_data['First Response Time P90'].mean(), 1),
                'sla_compliance': round(channel_data['% Responded Within SLA'].mean(), 3),
                'csat_score': round(channel_data['CSAT Score'].mean(), 2),
                'abandon_rate': round(channel_data['Abandon Rate'].mean(), 4),
                'escalation_rate': round(channel_data['Escalation Rate'].mean(), 4),
                'status': self._channel_status(channel_data)
            }
            performance.append(perf)
        
        return sorted(performance, key=lambda x: x['sla_compliance'], reverse=True)
    
    def queue_performance_table(self, operational_data):
        '''Detailed performance by queue'''
        performance = []
        for queue in operational_data['Queue'].unique():
            queue_data = operational_data[operational_data['Queue'] == queue]
            
            perf = {
                'queue': queue,
                'contacts': int(queue_data['Incoming Contacts'].sum()),
                'customers': int(queue_data['Unique Customers'].sum()),
                'response_time_median': round(queue_data['First Response Time Median'].mean(), 1),
                'sla_compliance': round(queue_data['% Responded Within SLA'].mean(), 3),
                'csat_score': round(queue_data['CSAT Score'].mean(), 2),
                'agents_scheduled': int(queue_data['Agent Scheduled'].sum()),
                'handle_time': round(queue_data['Agent Handle Time'].mean(), 1),
                'status': self._queue_status(queue_data)
            }
            performance.append(perf)
        
        return performance
    
    def _channel_status(self, channel_data):
        '''Determine channel health status'''
        compliance = channel_data['% Responded Within SLA'].mean()
        csat = channel_data['CSAT Score'].mean()
        
        if compliance >= 0.80 and csat >= 4.2:
            return 'Excellent'
        elif compliance >= 0.70 and csat >= 3.5:
            return 'Good'
        else:
            return 'At Risk'
    
    def _queue_status(self, queue_data):
        '''Determine queue health status'''
        compliance = queue_data['% Responded Within SLA'].mean()
        reopen = queue_data['Reopen Rate'].mean()
        
        if compliance >= 0.80 and reopen < 0.05:
            return 'Healthy'
        elif compliance >= 0.70 or reopen < 0.10:
            return 'Acceptable'
        else:
            return 'Needs Attention'
    
    def _calculate_health_status(self, operational_data):
        '''Calculate overall health status'''
        compliance = operational_data['% Responded Within SLA'].mean()
        csat = operational_data['CSAT Score'].mean()
        abandon = operational_data['Abandon Rate'].mean()
        
        if compliance >= 0.75 and csat >= 3.6 and abandon < 0.06:
            return 'Healthy'
        elif compliance >= 0.65 or csat >= 3.4:
            return 'At Risk'
        else:
            return 'Critical'
    
    def kpi_scorecard(self, operational_data):
        '''Generate KPI scorecard against targets'''
        scorecard = {}
        for kpi_name, threshold in self.kpi_thresholds.items():
            if kpi_name == 'sla_compliance':
                current = operational_data['% Responded Within SLA'].mean()
            elif kpi_name == 'csat_score':
                current = operational_data['CSAT Score'].mean()
            elif kpi_name == 'abandon_rate':
                current = operational_data['Abandon Rate'].mean()
            elif kpi_name == 'reopen_rate':
                current = operational_data['Reopen Rate'].mean()
            elif kpi_name == 'escalation_rate':
                current = operational_data['Escalation Rate'].mean()
            
            scorecard[kpi_name] = {
                'current': round(current, 3),
                'target': threshold,
                'status': 'Met' if current >= threshold else 'Missed',
                'gap': round(current - threshold, 3)
            }
        
        return scorecard

if __name__ == "__main__":
    dashboard = ChannelPerformanceDashboard()
    print("Channel Performance Dashboard v1.0 initialized")
    print("Views: Executive Summary, Channel Performance, Queue Performance, KPI Scorecard")
