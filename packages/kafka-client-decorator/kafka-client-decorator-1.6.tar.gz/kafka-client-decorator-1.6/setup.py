from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='kafka-client-decorator',
    version='1.6',
    license='Quantrium PVT LTD',
    description='A wrapper for confluent-kafka producer and consumer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Quantrium",
    author_email='firoz.mohammad@quantrium.ai',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://www.quantrium.ai/',
    keywords=['confluent-kafka', 'Kafka-producer', 'Kafka-consumer'],
    python_requires = ">=3.6",
    install_requires=[
          'confluent-kafka==2.0.2',
      ],

)