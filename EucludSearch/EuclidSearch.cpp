#include <iostream>
#include <ctime>
#include <string>
#include <fstream>
#include <vector>
#include <sstream>
#include <algorithm>
#include <map>

using namespace std;

const string vectors_file("../Vectors/Vectors.txt");
const string result_file("Results/Result_");
const string delimiter(",");
const int d = 128; //Размерность
const int q = 1000; // Количество запросов
int k_nearest = 50; // Количество ближайших соседей

double dist(vector<double> &a, vector<double> &b)
{
	double dist = 0.0;
	for(int i = 0; i < d; ++i)
		dist += (a[i] - b[i]) * (a[i] - b[i]);
	return dist;
}

int main(int argc, char **argv)
{
	if (argc > 2)
	{
		cout << "Usage: ./EuclidSearch <k_nearest>\n";
		return 0;
	}
	if (argc == 2)
		k_nearest = atoi(argv[1]);
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
    ofstream res_file(result_file + to_string(k_nearest));
    res_file << "EuclidSearch k = " << k_nearest << "\nQueries: " << q << "\n";
    int total_true = 0;
    int face_true = 0;
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
        map<string, int> freq;
    	for(int k = 1; k <= k_nearest; ++k)
    	{
    		string temp = vectors[v_dist[k].second].first;
    		if (freq.find(temp.substr(0, 8)) == freq.end())
    			freq[temp.substr(0, 8)] = 0;
    		freq[temp.substr(0, 8)] +=1;
    		if(temp.substr(0, 8) == queries[i].first.substr(0, 8))
            {
                count_true++;
    		    cout << "###  " << temp << "   " << v_dist[k].first << endl;
            }
    		else
    			cout << "     " << temp << "   " << v_dist[k].first << endl;
    	}

    	int max_freq = 0;
    	string face;
    	for (auto elem: freq)
    		if(elem.second > max_freq) {
    			max_freq = elem.second;
    			face = elem.first;
    		}
    	if (face == queries[i].first.substr(0, 8))
    		face_true++;

        total_true += count_true;
        total_time += ((end - start) / (double)CLOCKS_PER_SEC);
   		cout << "Searching time: " << ((end - start) / (double)CLOCKS_PER_SEC) << " seconds in " << count << " faces.\n" << endl;
    }
    
    res_file << "Search accuracy: " << 1.0*total_true/(q*k_nearest) << "\n";
    res_file << "Recognition accuracy: " << 1.0*face_true/q << "\n";
    res_file << "Time: " << total_time/q << "\n";
  	res_file.close();
  	file.close();

	return 0;
}