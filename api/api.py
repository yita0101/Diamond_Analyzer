from flask import Flask, jsonify, request
from lib.DiamondManager import DiamondManager
from config import Config
import os

app = Flask(__name__)
diamond_manager = DiamondManager(Config.get_fullnode_url())

@app.route('/analyse_address', methods=['GET'])
def analyse_address():
    address = request.args.get('address')
    
    if not address:
        return jsonify({
            'success': False,
            'message': 'Please provide a valid address',
            'code': 40001,
            'data': None
        }), 400
    
    try:
        results = diamond_manager.analyse_address_diamonds(address)

        diamonds_with_inscription = [r for r in results if r['has_hacds']]
        diamonds_without_inscription = [r for r in results if not r['has_hacds']]
        total_score = sum(r['score'] for r in results)
        
        return jsonify({
            'success': True,
            'message': 'Analysis completed',
            'code': 20000,
            'data': {
                'address': address,
                'total_diamonds': len(results),
                'total_score': total_score,
                'statistics': {
                    'with_inscription': {
                        'count': len(diamonds_with_inscription),
                        'score_sum': sum(d['score'] for d in diamonds_with_inscription),
                        'diamonds': [{'name': d['name'], 'score': d['score']} for d in diamonds_with_inscription]
                    },
                    'without_inscription': {
                        'count': len(diamonds_without_inscription),
                        'score_sum': sum(d['score'] for d in diamonds_without_inscription),
                        'diamonds': [{'name': d['name'], 'score': d['score']} for d in diamonds_without_inscription]
                    }
                }
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error occurred during analysis: {str(e)}',
            'code': 50000,
            'data': None
        }), 500

@app.route('/analyse_diamonds', methods=['GET'])
def analyse_diamonds():
    names = request.args.get('names', '')
    
    if not names:
        return jsonify({
            'success': False,
            'message': 'Please provide diamond names',
            'code': 40001,
            'data': None
        }), 400
    
    try:
        diamond_names = [name.strip().upper() for name in names.split(',')]
        
        invalid_names = [name for name in diamond_names if len(name) != 6]
        if invalid_names:
            return jsonify({
                'success': False,
                'message': f'Invalid diamond names: {", ".join(invalid_names)}',
                'code': 40002,
                'data': None
            }), 400
        
        results = []
        for name in diamond_names:
            score, has_hacds = diamond_manager.analyse_diamond(name)
            results.append({
                'name': name,
                'score': max(1, score),
                'has_hacds': has_hacds
            })
        
        diamonds_with_inscription = [r for r in results if r['has_hacds']]
        diamonds_without_inscription = [r for r in results if not r['has_hacds']]
        total_score = sum(r['score'] for r in results)
        
        return jsonify({
            'success': True,
            'message': 'Analysis completed',
            'code': 20000,
            'data': {
                'total_diamonds': len(results),
                'total_score': total_score,
                'statistics': {
                    'with_inscription': {
                        'count': len(diamonds_with_inscription),
                        'score_sum': sum(d['score'] for d in diamonds_with_inscription),
                        'diamonds': [{'name': d['name'], 'score': d['score']} for d in diamonds_with_inscription]
                    },
                    'without_inscription': {
                        'count': len(diamonds_without_inscription),
                        'score_sum': sum(d['score'] for d in diamonds_without_inscription),
                        'diamonds': [{'name': d['name'], 'score': d['score']} for d in diamonds_without_inscription]
                    }
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error occurred during analysis: {str(e)}',
            'code': 50000,
            'data': None
        }), 500

def run_development():
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    fullnode_url = Config.get_fullnode_url()
    print(f"Development server running at http://{host}:{port}")
    print(f"Fullnode URL: {fullnode_url}")
    app.run(
        host=host,
        port=port,
        debug=True
    )

def run_production():
    from waitress import serve
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    fullnode_url = Config.get_fullnode_url()
    print(f"Production server running at http://{host}:{port}")
    print(f"Fullnode URL: {fullnode_url}")
    serve(
        app,
        host=host,
        port=port
    )

if __name__ == '__main__':
    if Config.is_development():
        run_development()
    else:
        run_production()