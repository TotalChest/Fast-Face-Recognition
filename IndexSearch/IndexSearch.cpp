#include <iostream>
#include <ctime>
#include <string>
#include <fstream>
#include <vector>
#include <sstream>
#include <algorithm>
#include <omp.h>

using namespace std;

const string vectors_file("../Vectors/Vectors.txt");
const string delimiter(",");
const int d = 128; //Размерность
const int q = 10; // Количество запросов
const int k_nearest = 100; // Количество ближайших соседей
const int K = 400; // Количество центроидов
const int num_clasters = 3; // Количество соседних кластеров для поиска
const int threads = 8;

double dist(vector<double> &a, vector<double> &b)
{
	double dist = 0.0;
	for(int i = 0; i < d; ++i)
		dist += (a[i] - b[i]) * (a[i] - b[i]);
	return dist;
}

int main()
{
    omp_set_num_threads(threads);
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

    cout << "START LEARNING...\n";

    vector< vector<double> > centroids(K); // Вектор центроидов
    vector<int> member(count, 0); // Вектор меток

    for(int i = 0; i < K; ++i)
    {
        int index = rand() % count;
        centroids[i] = vectors[index].second;
    }

    for(int t = 0; t < 20; ++t)
    {    
        cout << "\r" << t << "/20" << flush;
        #pragma omp parallel for
        for(int i = 0; i < count; ++i)
        {
            double min = dist(vectors[i].second, centroids[0]);
            int cl = 0;
            for(int j = 1; j < K; ++j)
            {
                double distance = dist(vectors[i].second, centroids[j]);
                if(distance < min)
                {
                    min = distance;
                    cl = j;
                }
            }

            member[i] = cl;

        }

        #pragma omp parallel for
        for(int j = 0; j < K; ++j)
        {
            int num = 0;
            vector<double> temp(d,0);
            for(int i = 0; i < count; ++i)
                if(member[i] == j)
                {
                    ++num;
                    for(int g = 0; g < d; ++g)
                        temp[g] = temp[g] + vectors[i].second[g];
                }
            for(int i = 0; i < d; ++i)
                temp[i] /= num;
            centroids[j] = temp;
        }
    }
    cout << "\r" << "20/20" << endl;

    vector< vector < pair< string, vector<double> > > > InvertedIndex(K);
    for(int i = 0; i < count; ++i)
    {
        double min = dist(vectors[i].second, centroids[0]);
        int cl = 0;
        #pragma omp parallel for
        for(int j = 1; j < K; ++j)
        {
            double distance = dist(vectors[i].second, centroids[j]);
            if(distance < min)
            {
                min = distance;
                cl = j;
            }
        }
        
        InvertedIndex[cl].push_back({vectors[i].first, vectors[i].second});
    }

    vectors.clear();

    cout << "START SEARCHING...\n";

    for(int i = 0; i < q; ++i)
  	{
    	vector< pair<double, int> > claster_dist(K);
        vector< pair<double, string> > v_dist;

        clock_t start = clock();
        for(int j = 0; j < K; ++j)
        {
            claster_dist[j].second = j;
            claster_dist[j].first = dist(queries[i].second, centroids[j]);
        }
        sort(claster_dist.begin(), claster_dist.end());

        for(int j = 0; j < num_clasters; ++j)
            for(auto elem: InvertedIndex[claster_dist[j].second])
                v_dist.push_back({dist(queries[i].second, elem.second), elem.first});
        sort(v_dist.begin(), v_dist.end());
    	clock_t end = clock();

    	cout << "Query: " << queries[i].first << endl;

    	for(int k = 0; k < k_nearest; ++k)
    	{
    		string temp = v_dist[k].second;
    		if(temp.substr(0, 8) == queries[i].first.substr(0, 8))
    		    cout << "###  " << temp << "   " << v_dist[k].first << endl;
    		else
    			cout << "     " << temp << "   " << v_dist[k].first << endl;
    	}

   		cout << "Searching time: " << ((end - start) / (double)CLOCKS_PER_SEC) << " seconds in " << count << " faces.\n" << endl;
    }
    

  	file.close();

	return 0;
}