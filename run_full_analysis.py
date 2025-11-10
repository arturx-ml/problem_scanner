"""
Master script to run the complete Polymarket problem analysis pipeline
1. Collects data from Reddit and Twitter
2. Analyzes problems using NLP and sentiment analysis
3. Generates reports and visualizations
"""

import sys
from datetime import datetime

def main():
    print("\n" + "="*80)
    print(" "*20 + "POLYMARKET PROBLEM ANALYSIS PIPELINE")
    print("="*80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")
    
    # Step 1: Collect data
    print("STEP 1/2: Collecting data from Reddit and Twitter...")
    print("-" * 80)
    
    try:
        from collect_polymarket_data import PolymarketDataCollector
        
        collector = PolymarketDataCollector()
        df = collector.collect_all_data(days_back=30)
        
        if df.empty:
            print("\n❌ ERROR: No data collected. Please check your API credentials.")
            return False
            
        print("\n✓ Data collection completed successfully!")
        
    except Exception as e:
        print(f"\n❌ ERROR during data collection: {str(e)}")
        print("\nPlease ensure:")
        print("  1. Your .env file has valid Reddit and Twitter credentials")
        print("  2. All required packages are installed (pip install -r requirements.txt)")
        return False
    
    # Step 2: Analyze problems
    print("\n" + "="*80)
    print("STEP 2/2: Analyzing problems and generating reports...")
    print("-" * 80)
    
    try:
        from analyze_polymarket_problems import PolymarketProblemAnalyzer
        
        analyzer = PolymarketProblemAnalyzer()
        results = analyzer.run_full_analysis()
        
        if results is None:
            print("\n❌ ERROR: Analysis failed.")
            return False
            
        print("\n✓ Analysis completed successfully!")
        
    except Exception as e:
        print(f"\n❌ ERROR during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    # Success!
    print("\n" + "="*80)
    print(" "*30 + "SUCCESS!")
    print("="*80)
    print("\nThe following files have been generated:")
    print(f"  📊 Visualization: {results['viz_file']}")
    print(f"  📄 Text Report: {results['report_file']}")
    print(f"  💾 Problem Posts CSV: (check your directory)")
    print("\nYou can now:")
    print("  1. Review the visualization and report")
    print("  2. Open the Jupyter notebook for interactive analysis")
    print("  3. Use the findings to build solutions with Polymarket + Polygon API")
    print("\n" + "="*80)
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
