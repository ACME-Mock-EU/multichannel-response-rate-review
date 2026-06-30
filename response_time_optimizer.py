# Response Time Optimization Engine
# Analyze and optimize response times across multi-channel support

import pandas as pd
import numpy as np

class ResponseTimeOptimizer:
    def __init__(self):
        self.channel_tiers = {
            'synchronous': ['Live Chat', 'Phone', 'In-app Messaging', 'WhatsApp'],
            'asynchronous': ['Email', 'Web Form', 'X/Twitter DMs']
        }
        self.target_percentiles = {
            'p50': 60,      # Median target (minutes)
            'p90': 240      # 90th percentile target (minutes)
        }
    
    def categorize_channel(self, channel_name):
        '''Categorize channel by response type'''
        for tier, channels in self.channel_tiers.items():
            if any(c in channel_name for c in channels):
                return tier
        return 'other'
    
    def analyze_response_times(self, operational_data):
        '''Analyze response times by channel'''
        analysis = {}
        for channel in operational_data['Channel'].unique():
            channel_data = operational_data[operational_data['Channel'] == channel]
            
            median_rt = channel_data['First Response Time Median'].mean()
            p90_rt = channel_data['First Response Time P90'].mean()
            category = self.categorize_channel(channel)
            
            analysis[channel] = {
                'category': category,
                'median_response_time': median_rt,
                'p90_response_time': p90_rt,
                'contacts': len(channel_data),
                'sla_compliance': channel_data['% Responded Within SLA'].mean(),
                'status': self._health_status(median_rt, p90_rt, category)
            }
        
        return analysis
    
    def _health_status(self, median_rt, p90_rt, category):
        '''Determine channel health status'''
        if category == 'synchronous':
            if median_rt <= 5 and p90_rt <= 60:
                return 'Excellent'
            elif median_rt <= 30 and p90_rt <= 120:
                return 'Good'
            else:
                return 'Needs Improvement'
        else:  # asynchronous
            if median_rt <= 60 and p90_rt <= 240:
                return 'Good'
            elif median_rt <= 300 and p90_rt <= 1200:
                return 'Acceptable'
            else:
                return 'Needs Improvement'
    
    def identify_bottlenecks(self, operational_data):
        '''Identify channels with response time bottlenecks'''
        bottlenecks = []
        analysis = self.analyze_response_times(operational_data)
        
        for channel, metrics in analysis.items():
            if metrics['status'] == 'Needs Improvement':
                bottleneck = {
                    'channel': channel,
                    'category': metrics['category'],
                    'median_response_time': metrics['median_response_time'],
                    'p90_response_time': metrics['p90_response_time'],
                    'compliance_gap': 0.80 - metrics['sla_compliance'],
                    'recommendation': self._recommend_improvement(metrics)
                }
                bottlenecks.append(bottleneck)
        
        return bottlenecks
    
    def _recommend_improvement(self, metrics):
        '''Recommend improvements for slow channels'''
        if metrics['category'] == 'synchronous':
            if metrics['median_response_time'] > 30:
                return 'Increase staffing for live chat/phone'
            return 'Optimize routing and prioritization'
        else:
            if metrics['median_response_time'] > 300:
                return 'Automate email responses with templates'
            return 'Implement triage and priority queuing'
    
    def optimization_impact(self, operational_data, target_improvement_pct=10):
        '''Calculate impact of 10% response time improvement'''
        current_avg_compliance = operational_data['% Responded Within SLA'].mean()
        improved_compliance = min(1.0, current_avg_compliance * (1 + target_improvement_pct / 100))
        
        impact = {
            'current_compliance': round(current_avg_compliance, 3),
            'target_compliance': round(improved_compliance, 3),
            'improvement_pct': round((improved_compliance - current_avg_compliance) * 100, 2),
            'estimated_revenue_impact': 'Improved CSAT → Higher retention',
            'implementation_effort': 'Medium (staffing + automation)'
        }
        return impact

if __name__ == "__main__":
    optimizer = ResponseTimeOptimizer()
    print("Response Time Optimizer v1.0 initialized")
    print("Channels: Synchronous + Asynchronous | Optimization: Enabled")
