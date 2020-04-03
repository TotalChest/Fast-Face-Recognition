#include <iostream>
#include <ctime>
#include <string>
#include <fstream>
#include <vector>
#include <sstream>
#include <algorithm>

using namespace std;

const string vectors_file("../Vectors/Vectors.txt");
const string result_file("Result.txt");
const string delimiter(",");
const int d = 128; //Размерность
const int q = 1000; // Количество запросов
const int k_nearest = 50; // Количество ближайших соседей

double dist(vector<double> &a, vector<double> &b)
{
	double dist = 0.0;
	for(int i = 0; i < d; ++i)
		dist += (a[i] - b[i]) * (a[i] - b[i]);
	return dist;
}

int main()
{
	ifstream file(vectors_file);
	string str;
  	vector< pair< string, vector<double> > > vectors;
  	vector< pair< string, vector<double> > > queries(q);
 	size_t count = 0;

  	while ((getline(file, str)))
  	{
		size_t pos = 0;
		pos = str.find(delimiter);
		vectors.push_back({str.substr(0, pos), vector<double>()});
		str.erase(0, pos + delimiter.length());

		while ((pos = str.find(delimiter)) != string::npos)
		{
    		vectors[count].second.push_back(stod(str.substr(0, pos)));
   			str.erase(0, pos + delimiter.length());
		}
		vectors[count].second.push_back(stod(str));
		++count;
  	}

  	srand(unsigned(time(0)));
  	for(int i = 0; i < q; ++i)
  	{
    	int index = rand() % count;
    	queries[i] = vectors[index];
    }

    cout << "START SEARCHING...\n";
    ofstream res_file(result_file);
    res_file << "Queries: " << q << "\n";
    int total_true = 0;
    double total_time = 0;

    for(int i = 0; i < q; ++i)
  	{
    	vector< pair<double, int> > v_dist(count);

    	clock_t start = clock();
    	for(int j = 0; j < count; ++j)
    	{
    		v_dist[j].second = j;
    		v_dist[j].first = dist(queries[i].second, vectors[j].second);
    	}
    	sort(v_dist.begin(), v_dist.end());
    	clock_t end = clock();

    	cout << "Query: " << queries[i].first << endl;

        int count_true = 0;
    	for(int k = 0; k < k_nearest; ++k)
    	{
    		string temp = vectors[v_dist[k].second].first;
    		if(temp.substr(0, 8) == queries[i].first.substr(0, 8))
            {
                count_true++;
    		    cout << "###  " << temp << "   " << v_dist[k].first << endl;
            }
    		else
    			cout << "     " << temp << "   " << v_dist[k].first << endl;
    	}

        total_true += count_true;
        total_time += ((end - start) / (double)CLOCKS_PER_SEC);
   		cout << "Searching time: " << ((end - start) / (double)CLOCKS_PER_SEC) << " seconds in " << count << " faces.\n" << endl;
    }
    
    res_file << "Accuracy: " << 1.0*total_true/(q*k_nearest) << "\n";
    res_file << "Time: " << total_time/q << "\n";
  	res_file.close();
  	file.close();

	return 0;
}