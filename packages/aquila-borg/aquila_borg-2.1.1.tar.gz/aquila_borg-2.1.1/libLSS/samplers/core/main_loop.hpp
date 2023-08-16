/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/core/main_loop.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_SAMPLERS_MAINLOOP_HPP
#define __LIBLSS_SAMPLERS_MAINLOOP_HPP

#include <utility>
#include <list>
#include "libLSS/tools/console.hpp"
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/mcmc/global_state.hpp"

namespace LibLSS {

    class BlockLoop;
    class BlockSampler {
    public:
        typedef std::list<std::pair<std::shared_ptr<MarkovSampler>,int> > MCList;
    protected:
        MCList mclist;
        friend class BlockLoop;
    public:
        virtual void adder(BlockSampler& s) const {
            ConsoleContext<LOG_DEBUG> ctx("adder classic");
            s.mclist.insert(s.mclist.end(), mclist.begin(), mclist.end());
        }
        
        BlockSampler& operator<<(std::shared_ptr<MarkovSampler>&& s) {
            ConsoleContext<LOG_DEBUG> ctx("inserter shared_ptr");
            mclist.push_back(std::make_pair(s,1));
            return *this;
        }

        BlockSampler& operator<<(std::shared_ptr<MarkovSampler>& s) {
            ConsoleContext<LOG_DEBUG> ctx("inserter shared_ptr");
            mclist.push_back(std::make_pair(s,1));
            return *this;
        }
        
        BlockSampler& operator<<(MarkovSampler& s) {
            ConsoleContext<LOG_DEBUG> ctx("inserter");
            mclist.push_back(std::make_pair(std::shared_ptr<MarkovSampler>(&s, [](void *) {}), 1));
            return *this;
        }
        
        BlockSampler& operator<<(const BlockSampler& l) {
            ConsoleContext<LOG_DEBUG> ctx("adding block");
            l.adder(*this);
            return *this;
        }
    };
    
    class BlockLoop: public BlockSampler {
    private:
        int num_loop;
    protected:
        friend class BlockSampler;
        // Prevent any copy.
        BlockLoop(const BlockLoop& l) {
            num_loop = l.num_loop;
        }
        BlockLoop& operator=(const BlockLoop& l) { return *this; }
    public:
        BlockLoop(int loop = 1) : num_loop(loop) {}

        void setLoop(int loop) { num_loop = loop; }

        virtual void adder(BlockSampler& s) const {
            ConsoleContext<LOG_DEBUG> ctx("adder blockloop");
            ctx.print(boost::format("num_loop = %d") % num_loop);
            for (int l = 0; l < num_loop; l++)
                s.mclist.insert(s.mclist.end(), mclist.begin(), mclist.end());
        }
            
        ~BlockLoop() {}
    };
    
    class MainLoop: public BlockSampler {
    protected:
        MarkovState state;
        int mcmc_id;

        void show_splash();
    public:
        MainLoop();
        ~MainLoop();

        void initialize();
        void restore(const std::string& fname, bool flexible = false);
        void run();
        void save();
        void save_crash();
        void snap();

        MarkovState& get_state() { return state; }
        const MarkovState& get_state() const { return state; }
    
        void setStepID(int i) { mcmc_id = i; }
    };

}

#endif
