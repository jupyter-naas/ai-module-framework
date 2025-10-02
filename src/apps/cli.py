#!/usr/bin/env python3
"""
Simple CLI for the AI Module Framework
"""

import click
import requests
import json

@click.group()
def cli():
    """AI Module Framework CLI"""
    pass

@cli.command()
@click.option('--url', default='http://localhost:8000', help='API base URL')
def status(url):
    """Check agent status"""
    try:
        response = requests.get(f"{url}/")
        data = response.json()
        click.echo(f"✅ Agent is running at {url}")
        click.echo(f"Model URL: {data.get('model_url', 'Unknown')}")
    except Exception as e:
        click.echo(f"❌ Agent not available: {e}")

@cli.command()
@click.option('--url', default='http://localhost:8000', help='API base URL')
def list_ontologies(url):
    """List available ontologies"""
    try:
        response = requests.get(f"{url}/ontologies")
        data = response.json()
        ontologies = data.get('ontologies', [])
        if ontologies:
            click.echo("Available ontologies:")
            for ontology in ontologies:
                click.echo(f"  - {ontology}")
        else:
            click.echo("No ontologies found")
    except Exception as e:
        click.echo(f"❌ Error: {e}")

@cli.command()
@click.argument('ontology_name')
@click.option('--url', default='http://localhost:8000', help='API base URL')
def load_ontology(ontology_name, url):
    """Load an ontology from storage"""
    try:
        response = requests.post(
            f"{url}/load-ontology-from-storage",
            json={"message": ontology_name}
        )
        data = response.json()
        if 'message' in data:
            click.echo(f"✅ {data['message']}")
        else:
            click.echo(f"❌ {data.get('error', 'Unknown error')}")
    except Exception as e:
        click.echo(f"❌ Error: {e}")

@cli.command()
@click.argument('message')
@click.option('--url', default='http://localhost:8000', help='API base URL')
def chat(message, url):
    """Chat with the AI agent"""
    try:
        response = requests.post(
            f"{url}/chat",
            json={"message": message}
        )
        data = response.json()
        click.echo(f"🤖 {data.get('response', 'No response')}")
    except Exception as e:
        click.echo(f"❌ Error: {e}")

@cli.command()
@click.option('--url', default='http://localhost:8000', help='API base URL')
def context(url):
    """Show current ontology context"""
    try:
        response = requests.get(f"{url}/ontology-context")
        data = response.json()
        context = data.get('context', 'No context')
        click.echo("Current ontology context:")
        click.echo(context)
    except Exception as e:
        click.echo(f"❌ Error: {e}")

if __name__ == '__main__':
    cli()
